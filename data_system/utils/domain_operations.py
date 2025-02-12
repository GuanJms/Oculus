from typing import List

from data_system._enums import *


def parse_domain(domain_str, asset_domain=True, equity_domain=True, price_domain=True, option_domain=False, volatility_domain=False, model_domain=False):
    if isinstance(domain_str, list):
        return domain_str # already parsed
    # Split the domain string into parts
    parts = domain_str.split(".")

    # Define the sequence of enums for lookup, reflecting the hierarchical structure

    enum_sequence = []
    if asset_domain:
        enum_sequence.append(AssetDomain)
    if equity_domain:
        enum_sequence.append(EquityDomain)
    if price_domain:
        enum_sequence.append(PriceDomain)
    if option_domain:
        enum_sequence.append(OptionDomain)
    if volatility_domain:
        enum_sequence.append(VolatilityDomain)
    if model_domain:
        enum_sequence.append(ModelDomain)

    # Check if the parts list length matches the enum sequence length
    if len(parts) != len(enum_sequence):
        raise ValueError(
            "The domain string does not match the expected format or depth."
        )

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
        return ""
    return ".".join([domain.to_string() for domain in domains])


def fetch_domain(domain_type, domains: list, return_none=False):
    for domain in domains:
        if isinstance(domain, domain_type):
            return domain
    if return_none:
        return None
    raise ValueError(f"Domain Type {domain_type} is not found in {domains}")


# # Example usage
# domain_string = "EQUITY.STOCK.QUOTE"
# parsed_domains = parse_domain(domain_string)
# print(parsed_domains)
