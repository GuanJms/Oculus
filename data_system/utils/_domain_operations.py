from typing import List

from data_system._enums import *


def parse_domain(domain_str, asset_domina=True, equity_domina=True, price_domina=True):
    # Split the domain string into parts
    parts = domain_str.split('.')

    # Define the sequence of enums for lookup, reflecting the hierarchical structure

    enum_sequence = []
    if asset_domina:
        enum_sequence.append(AssetDomain)
    if equity_domina:
        enum_sequence.append(EquityDomain)
    if price_domina:
        enum_sequence.append(PriceDomain)

    # Check if the parts list length matches the enum sequence length
    if len(parts) != len(enum_sequence):
        raise ValueError("The domain string does not match the expected format or depth.")

    parsed_result = []
    for part, enum_class in zip(parts, enum_sequence):
        # Attempt to find the enum value; raise error if not found
        try:
            enum_value = enum_class[part.upper()]
            parsed_result.append(enum_value)
        except KeyError:
            raise ValueError(f"Unknown domain part: {part}")

    return parsed_result


def domain_to_chains(domains: List[DomainEnum]) -> str:
    if not domains:
        return ''
    return '.'.join([domain.to_string() for domain in domains])

# # Example usage
# domain_string = "EQUITY.STOCK.QUOTE"
# parsed_domains = parse_domain(domain_string)
# print(parsed_domains)
