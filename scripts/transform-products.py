#!/usr/bin/env python3
"""
Transform WooCommerce product CSV to Shopify-compatible CSV.

Usage:
    # Test batch: non-linen products with price AND image (191 products)
    python scripts/transform-products.py --test

    # All non-linen products (453 products)
    python scripts/transform-products.py

    # All products including linens (6,593 published)
    python scripts/transform-products.py --include-linens

    # Custom input file
    python scripts/transform-products.py --input path/to/export.csv

    # Dry run (stats only, no output file)
    python scripts/transform-products.py --dry-run
"""

import argparse
import csv
import os
import re
import sys
from pathlib import Path

# --- Default paths ---

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = Path.home() / "Local Sites/acepartyrental/app/public/wp-content/webtoffee_export/product_export_2024-10-10-05-07-49.csv"
DEFAULT_OUTPUT = REPO_ROOT / "planning/data-migration/shopify-import.csv"

# --- Shopify CSV columns ---
# https://help.shopify.com/en/manual/products/import-export/using-csv

SHOPIFY_HEADERS = [
    "Handle",
    "Title",
    "Body (HTML)",
    "Vendor",
    "Product Category",
    "Type",
    "Tags",
    "Published",
    "Option1 Name",
    "Option1 Value",
    "Option2 Name",
    "Option2 Value",
    "Variant SKU",
    "Variant Grams",
    "Variant Inventory Tracker",
    "Variant Inventory Policy",
    "Variant Fulfillment Service",
    "Variant Price",
    "Variant Compare At Price",
    "Variant Requires Shipping",
    "Variant Taxable",
    "Image Src",
    "Image Position",
    "Image Alt Text",
    "Gift Card",
    "SEO Title",
    "SEO Description",
    "Status",
]


def parse_woo_images(image_field):
    """Parse WooCommerce image field into list of (url, alt) tuples.

    WooCommerce format:
        url ! alt : text ! title : text ! desc : text ! caption : text
    Multiple images separated by ' | '
    """
    if not image_field or not image_field.strip():
        return []

    images = []
    for entry in image_field.split(" | "):
        entry = entry.strip()
        if not entry:
            continue

        parts = entry.split(" ! ")
        url = parts[0].strip()
        alt = ""

        for part in parts[1:]:
            part = part.strip()
            if part.startswith("alt :"):
                alt = part[5:].strip()
                break

        if url and url.startswith("http"):
            images.append((url, alt))

    return images


def parse_categories(cat_field):
    """Parse WooCommerce category field into structured data.

    Input: 'Chairs > Chiavari' or 'Tabletop > Dinnerware | Tabletop > Flatware'
    Returns: list of (top_level, sub_category) tuples
    """
    if not cat_field or not cat_field.strip():
        return []

    categories = []
    for cat in cat_field.split("|"):
        cat = cat.strip()
        if not cat:
            continue
        parts = [p.strip() for p in cat.split(" > ")]
        top = parts[0]
        sub = parts[1] if len(parts) > 1 else ""
        categories.append((top, sub))

    return categories


def is_linen_product(categories):
    """Check if any category is a linen category."""
    return any(top.lower() == "linens" for top, _ in categories)


def build_tags(row, categories):
    """Build Shopify tags from product data."""
    tags = []

    # Quote vs price tag
    price = row.get("regular_price", "").strip()
    if price and float(price) > 0:
        tags.append("has-price")
    else:
        tags.append("quote-only")

    # Category tags for filtering
    for top, sub in categories:
        tags.append(top)
        if sub:
            tags.append(sub)

    # Color attribute
    color = row.get("attribute:pa_color", "").strip()
    if color:
        tags.append(f"color:{color}")

    return ", ".join(tags)


def build_product_type(categories):
    """Map WooCommerce categories to Shopify product type."""
    if not categories:
        return ""
    # Use the top-level category as product type
    return categories[0][0]


def clean_html(content):
    """Light cleanup of product description HTML."""
    if not content:
        return ""
    # Strip leading/trailing whitespace
    content = content.strip()
    # Convert common Divi artifacts
    content = content.replace("[/et_pb_text]", "").replace("[et_pb_text]", "")
    # Remove empty paragraphs
    content = re.sub(r"<p>\s*</p>", "", content)
    return content


def get_seo_title(row):
    """Extract SEO title, falling back to post_title."""
    seo = row.get("meta:_yoast_wpseo_title", "").strip()
    if seo:
        # Yoast sometimes uses %%title%% placeholders
        seo = seo.replace("%%title%%", row.get("post_title", ""))
        seo = seo.replace("%%sep%%", "-")
        seo = seo.replace("%%sitename%%", "Ace Party & Tent Rental")
        seo = seo.strip(" -")
    return seo


def get_seo_description(row):
    """Extract SEO meta description."""
    return row.get("meta:_yoast_wpseo_metadesc", "").strip()


def transform_row(row):
    """Transform a single WooCommerce row to Shopify format.

    Returns a list of Shopify rows (multiple if product has multiple images).
    """
    categories = parse_categories(row.get("tax:product_cat", ""))
    images = parse_woo_images(row.get("images", ""))
    tags = build_tags(row, categories)

    price = row.get("regular_price", "").strip()
    sale_price = row.get("sale_price", "").strip()

    # Variant price: use regular_price, or 0 if empty
    variant_price = price if price else "0.00"
    compare_at = sale_price if sale_price and price and float(sale_price) < float(price) else ""

    # Option1: Color if present
    color = row.get("attribute:pa_color", "").strip()
    option1_name = "Color" if color else ""
    option1_value = color if color else ""

    # Option2: Size if present
    size = row.get("attribute:Size", "").strip()
    option2_name = "Size" if size else ""
    option2_value = size if size else ""

    # Build the primary product row
    primary = {
        "Handle": row.get("post_name", "").strip(),
        "Title": row.get("post_title", "").strip(),
        "Body (HTML)": clean_html(row.get("post_content", "")),
        "Vendor": "Ace Party & Tent Rental",
        "Product Category": "",
        "Type": build_product_type(categories),
        "Tags": tags,
        "Published": "TRUE",
        "Option1 Name": option1_name,
        "Option1 Value": option1_value,
        "Option2 Name": option2_name,
        "Option2 Value": option2_value,
        "Variant SKU": row.get("sku", "").strip(),
        "Variant Grams": "0",
        "Variant Inventory Tracker": "",
        "Variant Inventory Policy": "deny",
        "Variant Fulfillment Service": "manual",
        "Variant Price": variant_price,
        "Variant Compare At Price": compare_at,
        "Variant Requires Shipping": "FALSE",
        "Variant Taxable": "TRUE" if row.get("tax_status", "") == "taxable" else "FALSE",
        "Image Src": images[0][0] if images else "",
        "Image Position": "1" if images else "",
        "Image Alt Text": images[0][1] if images else row.get("post_title", "").strip(),
        "Gift Card": "FALSE",
        "SEO Title": get_seo_title(row),
        "SEO Description": get_seo_description(row),
        "Status": "active",
    }

    rows = [primary]

    # Additional rows for extra images (same Handle, blank everything else)
    for i, (url, alt) in enumerate(images[1:], start=2):
        img_row = {h: "" for h in SHOPIFY_HEADERS}
        img_row["Handle"] = primary["Handle"]
        img_row["Image Src"] = url
        img_row["Image Position"] = str(i)
        img_row["Image Alt Text"] = alt if alt else primary["Title"]
        rows.append(img_row)

    return rows


def main():
    parser = argparse.ArgumentParser(description="Transform WooCommerce CSV to Shopify format")
    parser.add_argument("--input", "-i", type=Path, default=DEFAULT_INPUT,
                        help="Path to WooCommerce product CSV")
    parser.add_argument("--output", "-o", type=Path, default=DEFAULT_OUTPUT,
                        help="Path for Shopify CSV output")
    parser.add_argument("--test", action="store_true",
                        help="Test batch: only non-linen products with price AND image")
    parser.add_argument("--include-linens", action="store_true",
                        help="Include linen products (default: non-linen only)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print stats without writing output file")
    parser.add_argument("--limit", type=int, default=0,
                        help="Limit output to N products (0 = no limit)")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    # --- Read and filter ---
    stats = {
        "total_read": 0,
        "skipped_draft": 0,
        "skipped_linen": 0,
        "skipped_grouped": 0,
        "skipped_no_price_image": 0,
        "included": 0,
        "with_images": 0,
        "with_price": 0,
        "quote_only": 0,
        "categories": {},
    }

    products = []

    with open(args.input, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            stats["total_read"] += 1

            # Skip drafts
            if row.get("post_status", "") != "publish":
                stats["skipped_draft"] += 1
                continue

            # Skip grouped parent products (children are imported as simple)
            if row.get("tax:product_type", "") == "grouped":
                stats["skipped_grouped"] += 1
                continue

            categories = parse_categories(row.get("tax:product_cat", ""))

            # Skip linens unless --include-linens
            if not args.include_linens and is_linen_product(categories):
                stats["skipped_linen"] += 1
                continue

            # Test mode: only products with price AND image
            price = row.get("regular_price", "").strip()
            has_price = price and float(price) > 0
            has_image = bool(row.get("images", "").strip())

            if args.test and not (has_price and has_image):
                stats["skipped_no_price_image"] += 1
                continue

            products.append(row)

            # Track stats
            if has_price:
                stats["with_price"] += 1
            else:
                stats["quote_only"] += 1
            if has_image:
                stats["with_images"] += 1

            for top, _ in categories:
                stats["categories"][top] = stats["categories"].get(top, 0) + 1

    # Apply limit
    if args.limit > 0:
        products = products[:args.limit]

    stats["included"] = len(products)

    # --- Print stats ---
    print(f"\n{'='*50}")
    print(f"WooCommerce to Shopify Product Transform")
    print(f"{'='*50}")
    print(f"Input:  {args.input}")
    print(f"Mode:   {'TEST (price + image only)' if args.test else 'ALL non-linen' if not args.include_linens else 'ALL products'}")
    print(f"\nRows read:        {stats['total_read']:>6}")
    print(f"Skipped draft:    {stats['skipped_draft']:>6}")
    print(f"Skipped grouped:  {stats['skipped_grouped']:>6}")
    print(f"Skipped linen:    {stats['skipped_linen']:>6}")
    if args.test:
        print(f"Skipped no $/img: {stats['skipped_no_price_image']:>6}")
    print(f"                  ------")
    print(f"Products to import: {stats['included']:>4}")
    print(f"  With price:     {stats['with_price']:>6}")
    print(f"  Quote-only:     {stats['quote_only']:>6}")
    print(f"  With images:    {stats['with_images']:>6}")

    if stats["categories"]:
        print(f"\nCategories:")
        for cat, count in sorted(stats["categories"].items(), key=lambda x: -x[1]):
            print(f"  {cat}: {count}")

    if args.dry_run:
        print(f"\n[DRY RUN] No output file written.")
        return

    # --- Transform and write ---
    args.output.parent.mkdir(parents=True, exist_ok=True)

    total_rows = 0
    with open(args.output, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SHOPIFY_HEADERS)
        writer.writeheader()

        for row in products:
            shopify_rows = transform_row(row)
            for sr in shopify_rows:
                writer.writerow(sr)
                total_rows += 1

    print(f"\nOutput: {args.output}")
    print(f"Rows written: {total_rows} ({stats['included']} products + extra image rows)")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
