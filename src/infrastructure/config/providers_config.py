from infrastructure.config.interfaces_config import website_lego_interface, website_bricklink_interface, \
    website_capi_cap_interface
from infrastructure.providers_impl.websites_interfaces_provider_impl import WebsitesInterfacesProviderImpl

websites_interfaces_provider = WebsitesInterfacesProviderImpl(
    website_lego_interface=website_lego_interface,
    website_bricklink_interface=website_bricklink_interface,
    website_capi_cap_interface=website_capi_cap_interface,

)