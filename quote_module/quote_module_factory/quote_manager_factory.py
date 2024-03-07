from configuration_module.configuration_manager import ConfigurationManager


class QuoteManagerFactory:

    @classmethod
    def create_quote_manager(cls, frequency_ms: int):
        from quote_module.quote_manager import QuoteManager
        MSD_COL_NAME = ConfigurationManager.get_MSD_COL_NAME()
        quote_manager = QuoteManager(MSD_COL_NAME=MSD_COL_NAME, frequency=frequency_ms)
        return quote_manager
