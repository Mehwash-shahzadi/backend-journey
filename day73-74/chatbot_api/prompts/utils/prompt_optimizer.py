import re
import logging

logger = logging.getLogger(__name__)


class PromptOptimizer:
    """Optimizes LLM prompts to reduce token usage while maintaining quality."""
    
    @staticmethod
    def estimate_tokens(text: str) -> int:
        """
        Rough estimate of token count (1 token ≈ 4 characters for English).
        
        Args:
            text: Text to estimate tokens for
            
        Returns:
            Estimated token count
        """
        # Average word length in English ~5 chars + 1 space = 6 chars per word
        # Gemini typically uses ~1 token per ~4 characters
        words = len(text.split())
        chars = len(text)
        # Use character-based estimate (more accurate for prompts)
        return max(words, chars // 4)
    
    @staticmethod
    def optimize_summarize_prompt(text: str) -> tuple[str, dict]:
        """
        Optimize summarization prompt.
        
        Optimization strategy:
        - Remove verbose instructions
        - Use direct language
        - Specify output format clearly but concisely
        
        Args:
            text: Text to summarize
            
        Returns:
            tuple: (optimized_prompt, optimization_stats)
        """
        # Original prompt estimate (typical 50 tokens base + text)
        original_base = 50
        original_total = original_base + PromptOptimizer.estimate_tokens(text)
        
        # Optimized prompt (Day 74)
        # Removed: "Be clear and capture", "main points" description
        # Kept: Core instruction + format + text
        optimized_prompt = f"""Summarize in 3-5 sentences:

{text}

Summary:"""
        
        optimized_total = PromptOptimizer.estimate_tokens(optimized_prompt)
        reduction_pct = ((original_total - optimized_total) / original_total) * 100 if original_total > 0 else 0
        
        stats = {
            "original_tokens": original_total,
            "optimized_tokens": optimized_total,
            "reduction_percent": round(reduction_pct, 1),
            "optimization_type": "summarize"
        }
        
        logger.info(f"Summarize prompt optimized: {stats['reduction_percent']}% reduction")
        
        return optimized_prompt, stats
    
    @staticmethod
    def optimize_moderate_prompt(text: str) -> tuple[str, dict]:
        """
        Optimize moderation prompt.
        
        Optimization strategy:
        - Remove "Return ONLY valid JSON (no other text)" redundancy
        - Simplify format specification
        - Direct and minimal
        
        Args:
            text: Text to moderate
            
        Returns:
            tuple: (optimized_prompt, optimization_stats)
        """
        original_base = 60  # Longer due to JSON format requirement
        original_total = original_base + PromptOptimizer.estimate_tokens(text)
        
        # Optimized version (Day 74)
        # Removed verbose explanations, kept essential JSON format
        optimized_prompt = f"""Analyze toxicity. Return JSON only:
{{"toxic": bool, "score": 0-1, "reasons": [list]}}

Text:
{text}

JSON:"""
        
        optimized_total = PromptOptimizer.estimate_tokens(optimized_prompt)
        reduction_pct = ((original_total - optimized_total) / original_total) * 100 if original_total > 0 else 0
        
        stats = {
            "original_tokens": original_total,
            "optimized_tokens": optimized_total,
            "reduction_percent": round(reduction_pct, 1),
            "optimization_type": "moderation"
        }
        
        logger.info(f"Moderation prompt optimized: {stats['reduction_percent']}% reduction")
        
        return optimized_prompt, stats
    
    @staticmethod
    def optimize_classify_prompt(text: str) -> tuple[str, dict]:
        """
        Optimize classification prompt.
        
        Optimization strategy:
        - Remove category explanation
        - Use category codes instead of names in instruction
        - Minimal format specification
        
        Args:
            text: Text to classify
            
        Returns:
            tuple: (optimized_prompt, optimization_stats)
        """
        original_base = 70  # Base for classification with categories
        original_total = original_base + PromptOptimizer.estimate_tokens(text)
        
        # Optimized version (Day 74)
        # Removed category descriptions, simplified format
        optimized_prompt = f"""Classify & sentiment. JSON only:
{{"category": "news|tech|sports|politics|entertainment|other", "sentiment": "positive|negative|neutral", "confidence": 0-1}}

Text:
{text}

JSON:"""
        
        optimized_total = PromptOptimizer.estimate_tokens(optimized_prompt)
        reduction_pct = ((original_total - optimized_total) / original_total) * 100 if original_total > 0 else 0
        
        stats = {
            "original_tokens": original_total,
            "optimized_tokens": optimized_total,
            "reduction_percent": round(reduction_pct, 1),
            "optimization_type": "classification"
        }
        
        logger.info(f"Classification prompt optimized: {stats['reduction_percent']}% reduction")
        
        return optimized_prompt, stats
    
    @staticmethod
    def optimize_generate_prompt(
        template_type: str,
        parameters: dict
    ) -> tuple[str, dict]:
        """
        Optimize text generation prompt.
        
        Optimization strategy:
        - Remove verbose descriptions
        - Use direct imperatives
        - Minimal instruction overhead
        
        Args:
            template_type: Type of content (email, blog, product_description)
            parameters: Template parameters (topic, tone, length, etc.)
            
        Returns:
            tuple: (optimized_prompt, optimization_stats)
        """
        base_tokens = 40  # Base instruction tokens
        param_tokens = sum(PromptOptimizer.estimate_tokens(str(v)) for v in parameters.values())
        original_total = base_tokens + param_tokens
        
        # Optimized prompts by template (Day 74)
        if template_type == "email":
            prompt = f"""Email: {parameters.get('topic', '')} ({parameters.get('tone', '')} tone, {parameters.get('length', 'medium')}):

"""
        elif template_type == "blog":
            prompt = f"""Blog post ({parameters.get('length', '500')} words, {parameters.get('tone', 'neutral')}):
Topic: {parameters.get('topic', '')}

"""
        elif template_type == "product_description":
            prompt = f"""Product description: {parameters.get('topic', '')}

"""
        else:
            prompt = ""
        
        optimized_total = PromptOptimizer.estimate_tokens(prompt)
        reduction_pct = ((original_total - optimized_total) / original_total) * 100 if original_total > 0 else 0
        
        stats = {
            "original_tokens": original_total,
            "optimized_tokens": optimized_total,
            "reduction_percent": round(reduction_pct, 1),
            "optimization_type": "generation"
        }
        
        logger.info(f"Generation prompt optimized ({template_type}): {stats['reduction_percent']}% reduction")
        
        return prompt, stats
    
    @staticmethod
    def optimize_chat_prompt(message: str, context: str = "") -> tuple[str, dict]:
        """
        Optimize chat message prompt.
        
        Optimization strategy:
        - Remove system message preamble if not needed
        - Include only essential context
        - Direct user message
        
        Args:
            message: User message
            context: Optional conversation context
            
        Returns:
            tuple: (optimized_prompt, optimization_stats)
        """
        # Original includes system message, instructions, etc.
        original_total = PromptOptimizer.estimate_tokens(message) + PromptOptimizer.estimate_tokens(context) + 20
        
        # Optimized: just context + message
        if context:
            optimized_prompt = f"{context}\n{message}"
        else:
            optimized_prompt = message
        
        optimized_total = PromptOptimizer.estimate_tokens(optimized_prompt)
        reduction_pct = ((original_total - optimized_total) / original_total) * 100 if original_total > 0 else 0
        
        stats = {
            "original_tokens": original_total,
            "optimized_tokens": optimized_total,
            "reduction_percent": round(reduction_pct, 1),
            "optimization_type": "chat"
        }
        
        logger.info(f"Chat prompt optimized: {stats['reduction_percent']}% reduction")
        
        return optimized_prompt, stats


# Convenience functions for quick access
def optimize_summarize(text: str) -> tuple[str, dict]:
    """Optimize summarize prompt."""
    return PromptOptimizer.optimize_summarize_prompt(text)


def optimize_moderate(text: str) -> tuple[str, dict]:
    """Optimize moderation prompt."""
    return PromptOptimizer.optimize_moderate_prompt(text)


def optimize_classify(text: str) -> tuple[str, dict]:
    """Optimize classification prompt."""
    return PromptOptimizer.optimize_classify_prompt(text)


def optimize_generate(template_type: str, parameters: dict) -> tuple[str, dict]:
    """Optimize generation prompt."""
    return PromptOptimizer.optimize_generate_prompt(template_type, parameters)


def optimize_chat(message: str, context: str = "") -> tuple[str, dict]:
    """Optimize chat message prompt."""
    return PromptOptimizer.optimize_chat_prompt(message, context)
