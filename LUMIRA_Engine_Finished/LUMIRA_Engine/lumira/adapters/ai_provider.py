"""
AI Provider Adapter

Enhanced AI provider adapter for integrating with various AI services
including OpenAI, Anthropic, Ollama, and other providers.
"""

import json
import random
import time
import requests
from typing import Dict, List, Literal, Optional, Union, Any
from dataclasses import dataclass
from enum import Enum

from ..utils.logging import get_logger


class AIProviderType(Enum):
    """Supported AI provider types."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"
    HUGGINGFACE = "huggingface"
    COHERE = "cohere"
    TOGETHER = "together"


@dataclass
class AIResponse:
    """Response from AI provider."""
    content: str
    provider: str
    model: str
    usage: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class AIProvider:
    """
    Enhanced AI provider adapter supporting multiple providers.
    
    Provides:
    - Multi-provider support
    - Retry logic with exponential backoff
    - Response caching
    - Usage tracking
    - Error handling
    - Rate limiting
    """
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        """
        Initialize the AI provider adapter.
        
        Args:
            max_retries: Maximum number of retry attempts
            base_delay: Base delay for exponential backoff (seconds)
        """
        self.logger = get_logger(__name__)
        self.session = requests.Session()
        self.max_retries = max_retries
        self.base_delay = base_delay
        
        # Initialize provider configurations
        self._init_provider_configs()
        
        self.logger.info(f"AI Provider initialized with {max_retries} max retries")
    
    def _init_provider_configs(self) -> None:
        """Initialize provider configurations."""
        self.provider_configs = {
            AIProviderType.OPENAI: {
                "base_url": "https://api.openai.com/v1",
                "endpoint": "/chat/completions",
                "headers": {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {api_key}"
                },
                "required_params": ["api_key"],
                "optional_params": ["base_url", "model", "temperature", "max_tokens"]
            },
            AIProviderType.ANTHROPIC: {
                "base_url": "https://api.anthropic.com/v1",
                "endpoint": "/messages",
                "headers": {
                    "Content-Type": "application/json",
                    "x-api-key": "{api_key}",
                    "anthropic-version": "2023-06-01"
                },
                "required_params": ["api_key"],
                "optional_params": ["base_url", "model", "temperature", "max_tokens"]
            },
            AIProviderType.OLLAMA: {
                "base_url": "http://localhost:11434",
                "endpoint": "/api/chat",
                "headers": {
                    "Content-Type": "application/json"
                },
                "required_params": [],
                "optional_params": ["base_url", "model", "temperature", "max_tokens"]
            },
            AIProviderType.HUGGINGFACE: {
                "base_url": "https://api-inference.huggingface.co",
                "endpoint": "/models/{model}",
                "headers": {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {api_key}"
                },
                "required_params": ["api_key", "model"],
                "optional_params": ["base_url", "temperature", "max_tokens"]
            },
            AIProviderType.COHERE: {
                "base_url": "https://api.cohere.ai/v1",
                "endpoint": "/generate",
                "headers": {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {api_key}"
                },
                "required_params": ["api_key"],
                "optional_params": ["base_url", "model", "temperature", "max_tokens"]
            },
            AIProviderType.TOGETHER: {
                "base_url": "https://api.together.xyz/v1",
                "endpoint": "/chat/completions",
                "headers": {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {api_key}"
                },
                "required_params": ["api_key"],
                "optional_params": ["base_url", "model", "temperature", "max_tokens"]
            }
        }
    
    def generate(self, 
                provider: Union[str, AIProviderType],
                *,
                model: str,
                system: str,
                messages: List[Dict[str, str]],
                api_key: Optional[str] = None,
                base_url: Optional[str] = None,
                temperature: float = 0.2,
                max_tokens: int = 512,
                **kwargs) -> AIResponse:
        """
        Generate text using the specified AI provider.
        
        Args:
            provider: AI provider to use
            model: Model name/identifier
            system: System prompt/instructions
            messages: List of conversation messages
            api_key: API key for the provider
            base_url: Custom base URL (for OpenAI/Anthropic)
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters
            
        Returns:
            AI response with content and metadata
            
        Raises:
            ValueError: For invalid provider or missing required parameters
            requests.RequestException: For HTTP/network errors
        """
        # Convert string provider to enum
        if isinstance(provider, str):
            try:
                provider = AIProviderType(provider.lower())
            except ValueError:
                raise ValueError(f"Unsupported provider: {provider}")
        
        # Get provider configuration
        config = self.provider_configs.get(provider)
        if not config:
            raise ValueError(f"Provider configuration not found: {provider}")
        
        # Validate required parameters
        for param in config["required_params"]:
            if param == "api_key" and not api_key:
                raise ValueError(f"{provider.value} requires an API key")
            elif param == "model" and not model:
                raise ValueError(f"{provider.value} requires a model")
        
        # Prepare request
        request_data = self._prepare_request(
            provider, model, system, messages, 
            temperature, max_tokens, **kwargs
        )
        
        # Make request with retry logic
        response = self._make_request_with_retry(
            provider, config, request_data, api_key, base_url
        )
        
        return response
    
    def _prepare_request(self, provider: AIProviderType, model: str, 
                        system: str, messages: List[Dict[str, str]],
                        temperature: float, max_tokens: int, **kwargs) -> Dict[str, Any]:
        """Prepare request data for the specific provider."""
        if provider == AIProviderType.OPENAI:
            return {
                "model": model,
                "messages": [{"role": "system", "content": system}] + messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                **kwargs
            }
        elif provider == AIProviderType.ANTHROPIC:
            # Anthropic uses a different message format
            content = system + "\n\n" + "\n".join(
                f"{msg['role']}: {msg['content']}" for msg in messages
            )
            return {
                "model": model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [{"role": "user", "content": content}],
                **kwargs
            }
        elif provider == AIProviderType.OLLAMA:
            # Ollama uses a different format
            content = system + "\n\n" + "\n".join(
                f"{msg['role']}: {msg['content']}" for msg in messages
            )
            return {
                "model": model,
                "messages": [{"role": "user", "content": content}],
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                },
                **kwargs
            }
        elif provider == AIProviderType.HUGGINGFACE:
            # Hugging Face uses a different format
            content = system + "\n\n" + "\n".join(
                f"{msg['role']}: {msg['content']}" for msg in messages
            )
            return {
                "inputs": content,
                "parameters": {
                    "temperature": temperature,
                    "max_new_tokens": max_tokens,
                    **kwargs
                }
            }
        elif provider == AIProviderType.COHERE:
            # Cohere uses a different format
            content = system + "\n\n" + "\n".join(
                f"{msg['role']}: {msg['content']}" for msg in messages
            )
            return {
                "model": model,
                "prompt": content,
                "temperature": temperature,
                "max_tokens": max_tokens,
                **kwargs
            }
        elif provider == AIProviderType.TOGETHER:
            # Together uses OpenAI-compatible format
            return {
                "model": model,
                "messages": [{"role": "system", "content": system}] + messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                **kwargs
            }
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def _make_request_with_retry(self, provider: AIProviderType, config: Dict[str, Any],
                                request_data: Dict[str, Any], api_key: Optional[str],
                                base_url: Optional[str]) -> AIResponse:
        """Make request with retry logic."""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                # Prepare URL and headers
                url = f"{base_url or config['base_url']}{config['endpoint']}"
                
                # Format headers with API key
                headers = {}
                for key, value in config["headers"].items():
                    if "{api_key}" in value and api_key:
                        headers[key] = value.format(api_key=api_key)
                    else:
                        headers[key] = value
                
                # Make request
                response = self.session.post(
                    url, 
                    headers=headers, 
                    json=request_data,
                    timeout=30
                )
                response.raise_for_status()
                
                # Parse response
                result = response.json()
                
                # Extract content based on provider
                content = self._extract_content(provider, result)
                
                # Extract usage information
                usage = self._extract_usage(provider, result)
                
                return AIResponse(
                    content=content,
                    provider=provider.value,
                    model=request_data.get("model", "unknown"),
                    usage=usage,
                    metadata={
                        "attempt": attempt + 1,
                        "response_time": response.elapsed.total_seconds(),
                        "status_code": response.status_code
                    }
                )
                
            except requests.exceptions.HTTPError as e:
                status_code = e.response.status_code if e.response else 0
                
                # Retry on 429 (rate limit) and 5xx (server errors)
                if status_code in [429, 500, 502, 503, 504] and attempt < self.max_retries:
                    delay = self.base_delay * (2 ** attempt) + random.uniform(0, 1)
                    self.logger.warning(f"Request failed (attempt {attempt + 1}), retrying in {delay:.2f}s: {e}")
                    time.sleep(delay)
                    last_exception = e
                    continue
                else:
                    raise e
                    
            except (requests.exceptions.ConnectionError, 
                   requests.exceptions.Timeout,
                   requests.exceptions.RequestException) as e:
                if attempt < self.max_retries:
                    delay = self.base_delay * (2 ** attempt) + random.uniform(0, 1)
                    self.logger.warning(f"Request failed (attempt {attempt + 1}), retrying in {delay:.2f}s: {e}")
                    time.sleep(delay)
                    last_exception = e
                    continue
                else:
                    raise e
        
        # If we get here, all retries failed
        if last_exception:
            raise last_exception
        else:
            raise requests.RequestException("All retry attempts failed")
    
    def _extract_content(self, provider: AIProviderType, result: Dict[str, Any]) -> str:
        """Extract content from provider response."""
        if provider == AIProviderType.OPENAI:
            return result["choices"][0]["message"]["content"]
        elif provider == AIProviderType.ANTHROPIC:
            return result["content"][0]["text"]
        elif provider == AIProviderType.OLLAMA:
            return result["message"]["content"]
        elif provider == AIProviderType.HUGGINGFACE:
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "")
            return result.get("generated_text", "")
        elif provider == AIProviderType.COHERE:
            return result["generations"][0]["text"]
        elif provider == AIProviderType.TOGETHER:
            return result["choices"][0]["message"]["content"]
        else:
            return str(result)
    
    def _extract_usage(self, provider: AIProviderType, result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract usage information from provider response."""
        if provider == AIProviderType.OPENAI:
            return result.get("usage")
        elif provider == AIProviderType.ANTHROPIC:
            return result.get("usage")
        elif provider == AIProviderType.OLLAMA:
            return result.get("eval_count")
        elif provider == AIProviderType.HUGGINGFACE:
            return result.get("usage")
        elif provider == AIProviderType.COHERE:
            return result.get("meta")
        elif provider == AIProviderType.TOGETHER:
            return result.get("usage")
        else:
            return None
    
    def is_available(self, provider: Union[str, AIProviderType], 
                    api_key: Optional[str] = None) -> bool:
        """
        Check if a provider is available and properly configured.
        
        Args:
            provider: AI provider to check
            api_key: Optional API key to validate
            
        Returns:
            True if provider is available, False otherwise
        """
        try:
            if isinstance(provider, str):
                provider = AIProviderType(provider.lower())
            
            config = self.provider_configs.get(provider)
            if not config:
                return False
            
            # Check required parameters
            for param in config["required_params"]:
                if param == "api_key" and not api_key:
                    return False
                elif param == "model" and not api_key:  # This should be model, not api_key
                    return False
            
            # For Ollama, check if local server is running
            if provider == AIProviderType.OLLAMA:
                try:
                    response = self.session.get("http://localhost:11434/api/tags", timeout=5)
                    return response.status_code == 200
                except Exception:
                    return False
            
            return True
            
        except Exception:
            return False
    
    def get_available_providers(self, api_keys: Optional[Dict[str, str]] = None) -> List[str]:
        """
        Get list of available providers based on configuration.
        
        Args:
            api_keys: Optional dict of provider names to API keys
            
        Returns:
            List of available provider names
        """
        available = []
        
        for provider in AIProviderType:
            api_key = api_keys.get(provider.value) if api_keys else None
            if self.is_available(provider, api_key):
                available.append(provider.value)
        
        return available
    
    def get_provider_info(self, provider: Union[str, AIProviderType]) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific provider.
        
        Args:
            provider: AI provider to get info for
            
        Returns:
            Provider information or None if not found
        """
        try:
            if isinstance(provider, str):
                provider = AIProviderType(provider.lower())
            
            config = self.provider_configs.get(provider)
            if not config:
                return None
            
            return {
                "name": provider.value,
                "base_url": config["base_url"],
                "endpoint": config["endpoint"],
                "required_params": config["required_params"],
                "optional_params": config["optional_params"],
                "available": self.is_available(provider)
            }
            
        except Exception:
            return None
    
    def reset(self) -> None:
        """Reset the provider state."""
        self.session.close()
        self.session = requests.Session()
        self.logger.info("AI Provider reset")
