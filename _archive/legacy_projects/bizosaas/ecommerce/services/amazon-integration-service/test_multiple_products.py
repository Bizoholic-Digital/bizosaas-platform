#!/usr/bin/env python3
"""
Test Multiple Products - Validate workflow with different sports/fitness products
"""

import asyncio
import json
from datetime import datetime
from test_workflow_direct import MockWorkflowProcessor, Colors, print_header, print_section, print_success, print_info, format_price

async def test_multiple_products():
    """Test workflow with multiple verified products"""

    print_header("MULTI-PRODUCT WORKFLOW TEST")
    print(f"{Colors.OKCYAN}Testing automation with 3 different sports/fitness products{Colors.ENDC}\n")

    # Test products
    test_products = [
        ("B0DX1QJFK4", "Boldfit Yoga Mat", 0.30),
        ("B08D8J5BVR", "Boldfit Resistance Band Red", 0.35),
        ("B08H7XCSTS", "Boldfit Resistance Band Purple", 0.28),
    ]

    processor = MockWorkflowProcessor()
    results = []

    for asin, name, margin in test_products:
        print_section(f"PROCESSING: {name}")
        print_info("ASIN", asin)
        print_info("Target Margin", f"{margin * 100}%")

        try:
            result = await processor.execute_workflow(asin, margin)

            if result["success"]:
                product = result["product_data"]
                pricing = result["pricing_data"]
                ai = result["ai_content"]

                print_success("Workflow completed successfully")
                print_info("Source Price", format_price(product["price"]))
                print_info("Selling Price", format_price(pricing["selling_price"]))
                print_info("Profit", format_price(pricing["profit_amount"]))
                print_info("Margin", f"{pricing['profit_margin']:.1f}%")
                print_info("Execution Time", f"{result['execution_time']:.2f}s")
                print_info("Quality Score", f"{ai['quality_score'] * 100:.1f}%")

                results.append({
                    "asin": asin,
                    "name": name,
                    "source_price": product["price"],
                    "selling_price": pricing["selling_price"],
                    "profit": pricing["profit_amount"],
                    "margin": pricing["profit_margin"],
                    "execution_time": result["execution_time"],
                    "quality_score": ai["quality_score"]
                })
            else:
                print(f"{Colors.FAIL}Failed{Colors.ENDC}")

        except Exception as e:
            print(f"{Colors.FAIL}Error: {str(e)}{Colors.ENDC}")

        print()

    # Summary
    print_header("BATCH PROCESSING SUMMARY")

    if results:
        print_section("RESULTS TABLE")
        print(f"\n{'ASIN':<15} {'Product':<30} {'Source':<10} {'Selling':<10} {'Profit':<10} {'Margin':<8} {'Time':<6}")
        print("-" * 95)

        total_profit = 0
        total_time = 0

        for r in results:
            print(f"{r['asin']:<15} {r['name'][:28]:<30} {format_price(r['source_price']):<10} "
                  f"{format_price(r['selling_price']):<10} {format_price(r['profit']):<10} "
                  f"{r['margin']:.1f}%     {r['execution_time']:.2f}s")
            total_profit += r['profit']
            total_time += r['execution_time']

        print("-" * 95)
        print(f"\n{Colors.OKGREEN}Total Products Processed: {len(results)}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}Total Profit Potential: {format_price(total_profit)}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}Average Processing Time: {total_time / len(results):.2f}s{Colors.ENDC}")
        print(f"{Colors.OKGREEN}Average Quality Score: {sum(r['quality_score'] for r in results) / len(results) * 100:.1f}%{Colors.ENDC}")

        # Save summary
        summary_file = f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(summary_file, 'w') as f:
            json.dump({
                "test_date": datetime.now().isoformat(),
                "total_products": len(results),
                "results": results,
                "summary": {
                    "total_profit_potential": total_profit,
                    "average_processing_time": total_time / len(results),
                    "average_quality_score": sum(r['quality_score'] for r in results) / len(results)
                }
            }, f, indent=2)

        print(f"\n{Colors.OKGREEN}Summary saved to: {summary_file}{Colors.ENDC}")

    print(f"\n{Colors.OKGREEN}{Colors.BOLD}✅ Multi-product test completed successfully!{Colors.ENDC}\n")

if __name__ == "__main__":
    asyncio.run(test_multiple_products())
