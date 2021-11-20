<?php

use Symfony\Component\DependencyInjection\Argument\RewindableGenerator;

// This file has been auto-generated by the Symfony Dependency Injection Component for internal use.
// Returns the public 'prestashop.adapter.query_handler.get_cart_information_handler' shared service.

return $this->services['prestashop.adapter.query_handler.get_cart_information_handler'] = new \PrestaShop\PrestaShop\Adapter\Cart\QueryHandler\GetCartForOrderCreationHandler(${($_ = isset($this->services['prestashop.core.localization.locale.context_locale']) ? $this->services['prestashop.core.localization.locale.context_locale'] : $this->load('getPrestashop_Core_Localization_Locale_ContextLocaleService.php')) && false ?: '_'}, ${($_ = isset($this->services['prestashop.adapter.legacy.context']) ? $this->services['prestashop.adapter.legacy.context'] : $this->getPrestashop_Adapter_Legacy_ContextService()) && false ?: '_'}->getContext()->language->id, ${($_ = isset($this->services['prestashop.adapter.legacy.context']) ? $this->services['prestashop.adapter.legacy.context'] : $this->getPrestashop_Adapter_Legacy_ContextService()) && false ?: '_'}->getContext()->link, ${($_ = isset($this->services['prestashop.adapter.context_state_manager']) ? $this->services['prestashop.adapter.context_state_manager'] : $this->load('getPrestashop_Adapter_ContextStateManagerService.php')) && false ?: '_'}, ${($_ = isset($this->services['translator.default']) ? $this->services['translator.default'] : $this->getTranslator_DefaultService()) && false ?: '_'});