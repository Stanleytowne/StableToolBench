#!/usr/bin/env python
"""
截获StableToolBench推理时第一个query的完整对话历史
包括输入、输出、function调用等，用于检查格式
"""

import sys
import os
import json
import argparse
from termcolor import colored

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from toolbench.inference.Downstream_tasks.rapidapi import pipeline_runner


class ConversationCapture:
    """捕获对话历史的回调类"""
    
    def __init__(self, output_file="captured_conversation.json"):
        self.output_file = output_file
        self.captured = False
        self.conversation_data = {
            "query": None,
            "conversations": [],
            "full_messages": [],
            "step_by_step": []
        }
    
    def on_tool_retrieval_start(self):
        pass
    
    def on_tool_retrieval_end(self, tools=None):
        if not self.captured:
            print(colored(f"[Capture] Retrieved {len(tools) if tools else 0} tools", "cyan"))
    
    def on_request_start(self, user_input=None, method=None):
        if not self.captured:
            self.conversation_data["query"] = user_input
            self.conversation_data["method"] = method
            print(colored(f"[Capture] Starting to capture query: {user_input[:100]}...", "green"))
    
    def on_request_end(self, chain=None, outputs=None):
        if not self.captured and chain is not None:
            # chain是terminal_node[0]，需要获取完整的消息历史
            # 从terminal node向上遍历获取所有消息
            messages = []
            node = chain
            
            # 收集所有节点的消息
            node_messages = []
            while node is not None:
                if hasattr(node, 'messages') and node.messages:
                    node_messages.append((node, node.messages))
                if hasattr(node, 'father'):
                    node = node.father
                else:
                    break
            
            # 从根节点开始构建完整消息序列
            if node_messages:
                # 使用最后一个节点的消息（应该是最完整的）
                messages = node_messages[-1][1]
            
            # 转换为StableToolBench格式的conversations
            conversations = []
            
            for msg in messages:
                role = msg.get('role', '')
                content = msg.get('content', '')
                
                if role == 'system':
                    conversations.append({
                        "from": "system",
                        "value": content
                    })
                elif role == 'user':
                    conversations.append({
                        "from": "user",
                        "value": content
                    })
                elif role == 'assistant':
                    conversations.append({
                        "from": "assistant",
                        "value": content
                    })
                elif role in ['function', 'tool']:
                    # Function response
                    conversations.append({
                        "from": "function",
                        "value": content
                    })
            
            # 获取步骤信息
            step_by_step = []
            node = chain
            while node is not None:
                if hasattr(node, 'node_type') and node.node_type:
                    step_info = {
                        "node_type": getattr(node, 'node_type', ''),
                        "description": getattr(node, 'description', ''),
                        "observation": getattr(node, 'observation', ''),
                        "observation_code": getattr(node, 'observation_code', None)
                    }
                    step_by_step.insert(0, step_info)
                if hasattr(node, 'father'):
                    node = node.father
                else:
                    break
            
            self.conversation_data["conversations"] = conversations
            self.conversation_data["full_messages"] = messages
            self.conversation_data["step_by_step"] = step_by_step
            self.conversation_data["outputs"] = outputs
            
            # 保存到文件
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_data, f, indent=2, ensure_ascii=False)
            
            print(colored(f"[Capture] Conversation captured and saved to {self.output_file}", "green"))
            print(colored(f"[Capture] Total messages: {len(messages)}", "green"))
            print(colored(f"[Capture] Total steps: {len(step_by_step)}", "green"))
            
            # 打印格式化的对话
            self.print_conversation()
            
            self.captured = True
    
    def print_conversation(self):
        """打印格式化的对话"""
        print("\n" + "="*80)
        print(colored("CAPTURED CONVERSATION", "yellow", attrs=['bold']))
        print("="*80 + "\n")
        
        for i, conv in enumerate(self.conversation_data["conversations"]):
            role = conv["from"]
            content = conv["value"]
            
            if role == "system":
                print(colored(f"[SYSTEM]", "red", attrs=['bold']))
                print(content[:500] + "..." if len(content) > 500 else content)
            elif role == "user":
                print(colored(f"[USER]", "green", attrs=['bold']))
                print(content)
            elif role == "assistant":
                print(colored(f"[ASSISTANT]", "blue", attrs=['bold']))
                print(content)
            elif role == "function":
                print(colored(f"[FUNCTION]", "magenta", attrs=['bold']))
                print(content)
            
            print("-" * 80)
        
        print("\n" + "="*80)
        print(colored("STEP BY STEP", "yellow", attrs=['bold']))
        print("="*80 + "\n")
        
        for i, step in enumerate(self.conversation_data["step_by_step"]):
            print(colored(f"Step {i+1}: {step['node_type']}", "cyan", attrs=['bold']))
            if step['description']:
                print(f"  Description: {step['description'][:200]}...")
            if step['observation']:
                print(f"  Observation: {step['observation'][:200]}...")
            print()


def main():
    parser = argparse.ArgumentParser(description='Capture first query conversation from StableToolBench')
    parser.add_argument('--tool_root_dir', type=str, required='data/toolenv/tools', help='Tool root directory')
    parser.add_argument('--backbone_model', type=str, default="toolllama", help='Backbone model')
    parser.add_argument('--model_path', type=str, default='ToolBench/ToolLLaMA-2-7b-v2', help='Model path')
    parser.add_argument('--max_observation_length', type=int, default=1024, help='Max observation length')
    parser.add_argument('--method', type=str, default="CoT@1", help='Method')
    parser.add_argument('--input_query_file', type=str, required='StableToolBench/solvable_queries_example/test_instruction/G1_instruction.json', help='Input query file')
    parser.add_argument('--output_file', type=str, default="captured_conversation.json", help='Output file')
    parser.add_argument('--max_sequence_length', type=int, default=8192, help='Max sequence length')
    parser.add_argument('--max_source_sequence_length', type=int, default=4096, help='Max source sequence length')
    parser.add_argument('--toolbench_key', type=str, default="", help='ToolBench key')
    parser.add_argument('--service_url', type=str, default="http://localhost:8080/virtual", help='Service URL')
    
    args = parser.parse_args()
    
    # 设置环境变量
    os.environ['SERVICE_URL'] = args.service_url
    
    # 创建捕获器
    capture = ConversationCapture(output_file=args.output_file)
    
    # 创建pipeline runner
    runner = pipeline_runner(args, add_retrieval=False, process_id=0, server=False)
    
    # 只处理第一个任务
    if len(runner.task_list) == 0:
        print(colored("No tasks found!", "red"))
        return
    
    print(colored(f"Total tasks: {len(runner.task_list)}", "yellow"))
    print(colored("Processing first task only for capture...", "yellow"))
    
    # 处理第一个任务
    first_task = runner.task_list[0]
    result = runner.run_single_task(
        *first_task,
        retriever=None,
        process_id=0,
        callbacks=[capture],
        server=None
    )
    
    print(colored(f"\nCapture complete! Saved to {args.output_file}", "green", attrs=['bold']))


if __name__ == "__main__":
    main()
