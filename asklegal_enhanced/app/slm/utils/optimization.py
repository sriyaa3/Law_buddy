import os
import json
from typing import Dict, Any

class ModelOptimizer:
    """Model optimization utilities for SLMs"""
    
    def __init__(self):
        """Initialize the model optimizer"""
        self.optimization_config = {
            "quantization": {
                "enabled": True,
                "method": "Q4_K_M",  # Default quantization method
                "bits": 4
            },
            "pruning": {
                "enabled": False,
                "sparsity": 0.2
            },
            "knowledge_distillation": {
                "enabled": False,
                "teacher_model": None
            }
        }
    
    def get_optimization_config(self) -> Dict[str, Any]:
        """
        Get current optimization configuration
        
        Returns:
            Dict[str, Any]: Optimization configuration
        """
        return self.optimization_config
    
    def set_quantization_method(self, method: str, bits: int = 4):
        """
        Set quantization method
        
        Args:
            method (str): Quantization method (Q4_K_M, Q5_K_M, etc.)
            bits (int): Number of bits for quantization
        """
        self.optimization_config["quantization"]["method"] = method
        self.optimization_config["quantization"]["bits"] = bits
        self.optimization_config["quantization"]["enabled"] = True
    
    def enable_pruning(self, sparsity: float = 0.2):
        """
        Enable model pruning
        
        Args:
            sparsity (float): Sparsity level (0.0 to 1.0)
        """
        self.optimization_config["pruning"]["enabled"] = True
        self.optimization_config["pruning"]["sparsity"] = sparsity
    
    def enable_knowledge_distillation(self, teacher_model: str):
        """
        Enable knowledge distillation
        
        Args:
            teacher_model (str): Path or name of teacher model
        """
        self.optimization_config["knowledge_distillation"]["enabled"] = True
        self.optimization_config["knowledge_distillation"]["teacher_model"] = teacher_model
    
    def get_model_size_reduction(self, original_size_gb: float, model_name: str = None) -> Dict[str, float]:
        """
        Estimate model size reduction with current optimization settings
        
        Args:
            original_size_gb (float): Original model size in GB
            model_name (str, optional): Model name for specific optimizations
            
        Returns:
            Dict[str, float]: Size reduction information
        """
        reduction_info = {
            "original_size_gb": original_size_gb,
            "quantized_size_gb": original_size_gb,
            "reduction_percentage": 0.0,
            "recommended": "Q4_K_M"  # Default recommendation
        }
        
        # Apply quantization reduction
        if self.optimization_config["quantization"]["enabled"]:
            method = self.optimization_config["quantization"]["method"]
            bits = self.optimization_config["quantization"]["bits"]
            
            # Rough estimates for size reduction
            if bits == 4:
                if method == "Q4_K_M":
                    reduction_info["quantized_size_gb"] = original_size_gb * 0.27  # ~73% reduction
                    reduction_info["recommended"] = "Q4_K_M"
                else:
                    reduction_info["quantized_size_gb"] = original_size_gb * 0.30  # ~70% reduction
            elif bits == 5:
                reduction_info["quantized_size_gb"] = original_size_gb * 0.35  # ~65% reduction
                reduction_info["recommended"] = "Q5_K_M"
            elif bits == 8:
                reduction_info["quantized_size_gb"] = original_size_gb * 0.50  # ~50% reduction
        
        # Calculate reduction percentage
        if original_size_gb > 0:
            reduction_info["reduction_percentage"] = (
                (original_size_gb - reduction_info["quantized_size_gb"]) / original_size_gb
            ) * 100
        
        return reduction_info
    
    def generate_optimization_report(self, model_name: str, original_size_gb: float) -> str:
        """
        Generate optimization report for a model
        
        Args:
            model_name (str): Name of the model
            original_size_gb (float): Original model size in GB
            
        Returns:
            str: Optimization report
        """
        size_info = self.get_model_size_reduction(original_size_gb, model_name)
        
        report = f"""
Model Optimization Report for {model_name}
=======================================

Original Size: {size_info['original_size_gb']:.2f} GB
Quantized Size: {size_info['quantized_size_gb']:.2f} GB
Size Reduction: {size_info['reduction_percentage']:.1f}%

Recommended Quantization: {size_info['recommended']}

Optimization Settings:
- Quantization: {'Enabled' if self.optimization_config['quantization']['enabled'] else 'Disabled'}
  Method: {self.optimization_config['quantization']['method']}
  Bits: {self.optimization_config['quantization']['bits']}
- Pruning: {'Enabled' if self.optimization_config['pruning']['enabled'] else 'Disabled'}
  Sparsity: {self.optimization_config['pruning']['sparsity'] if self.optimization_config['pruning']['enabled'] else 'N/A'}
- Knowledge Distillation: {'Enabled' if self.optimization_config['knowledge_distillation']['enabled'] else 'Disabled'}
  Teacher Model: {self.optimization_config['knowledge_distillation']['teacher_model'] if self.optimization_config['knowledge_distillation']['enabled'] else 'N/A'}

Performance Impact:
- Memory Usage: Significantly reduced
- Inference Speed: May vary (typically faster on CPU)
- Accuracy: Minimal loss with Q4_K_M quantization
"""
        
        return report.strip()

# Global instance
model_optimizer = ModelOptimizer()