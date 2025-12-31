# 论文转换系统：整合过程之圆与文字穿刺球体模型
# 基于 `过程之圆.py` 和 `文字穿刺的球体.py`

import time
import logging
import json
import os
from typing import Dict, List, Optional
from docx import Document

# 导入过程之圆系统
from 过程之圆 import ProcessCircle, DataAnalysisRuler, verification_system
# 导入文字穿刺球体系统
from 文字穿刺的球体 import Sphere, EightSphereVerification

# 配置日志
handlers = [logging.FileHandler('论文转换系统.log', encoding='utf-8'), logging.StreamHandler()]
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)-5s - %(message)s',
    datefmt='%H:%M:%S',
    handlers=handlers
)
logger = logging.getLogger(__name__)

class PaperConverter:
    """
    论文转换系统主类：整合过程之圆与文字穿刺球体模型
    
    核心功能：
    - 论文的迭代转换处理
    - 文字与球体的相互作用分析
    - 自指循环的转换优化
    - 转换结果的完整性验证
    """
    
    def __init__(self, paper_title: str, max_iterations: int = 5):
        """
        初始化论文转换系统
        
        参数：
        - paper_title: 论文标题
        - max_iterations: 最大迭代转换次数
        """
        logger.info(f"[论文转换系统] 初始化：{paper_title}")
        
        # 验证系统完整性
        try:
            verification_system.verify_integrity()
            logger.info("[论文转换系统] 8球体联合验证通过")
        except RuntimeError as e:
            logger.error(f"[论文转换系统] 验证失败: {e}")
            raise
        
        # 初始化过程之圆
        self.process_circle = ProcessCircle(
            name=f"{paper_title}_转换引擎", 
            max_iterations=max_iterations
        )
        
        # 初始化数据分析尺子
        self.analysis_ruler = DataAnalysisRuler(
            name=f"{paper_title}_分析尺子",
            max_iterations=max_iterations
        )
        
        # 初始化文字穿刺球体
        self.text_sphere = Sphere(radius=1.8, center=(8.75, 9.0, 0.0))  # 使用标准3D参数
        
        # 初始化系统状态
        self.paper_title = paper_title
        self.original_content = ""
        self.processed_content = ""
        self.conversion_history = []
        self.analysis_results = []
        self.sphere_intersections = []
    
    def load_paper(self, content: str):
        """
        加载论文内容
        
        参数：
        - content: 论文文本内容
        """
        logger.info(f"[论文转换系统] 加载论文，长度：{len(content)} 字符")
        self.original_content = content
        self.processed_content = content
        
        # 加载数据到分析尺子
        # 将文本转换为可分析的数值序列（字符编码）
        char_codes = [ord(c) for c in content[:1000]]  # 取前1000字符进行分析
        self.analysis_ruler.load_data(char_codes)
    
    def load_paper_from_file(self, file_path: str):
        """
        从文件加载论文内容（支持文本文件、.docx和.doc文件）
        
        参数：
        - file_path: 文件路径
        """
        logger.info(f"[论文转换系统] 从文件加载论文：{file_path}")
        
        # 根据文件扩展名选择读取方式
        if file_path.lower().endswith('.docx'):
            # 读取Word文档
            doc = Document(file_path)
            content = []
            for paragraph in doc.paragraphs:
                content.append(paragraph.text)
            content = '\n'.join(content)
        elif file_path.lower().endswith('.doc'):
            # 使用pywin32读取旧版Word文档
            import win32com.client
            
            # 启动Word应用程序
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = False
            
            try:
                # 打开文档
                doc = word.Documents.Open(file_path)
                
                # 读取文档内容
                content = doc.Content.Text
                
                # 关闭文档
                doc.Close()
            finally:
                # 退出Word应用程序
                word.Quit()
        else:
            # 尝试使用多种编码读取文本文件
            encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16']
            content = None
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                raise ValueError(f"无法使用任何支持的编码读取文件: {file_path}")
        
        self.load_paper(content)
    
    def _process_text_with_sphere(self, text: str) -> Dict:
        """
        使用文字穿刺球体处理文本
        
        参数：
        - text: 待处理的文本
        
        返回：
        - Dict: 处理结果
        """
        logger.debug(f"[球体处理] 分析文本片段：{text[:50]}...")
        
        # 检测文字与球体的相交
        intersections = self.text_sphere.text_intersection(text)
        
        # 计算文本的球体特征（基于字符编码）
        char_codes = [ord(c) for c in text]
        total_code = sum(char_codes)
        avg_code = total_code / len(char_codes) if char_codes else 0
        
        # 计算违和强度（简化实现）
        # 这里使用字符编码总和与球体半径的关系作为违和强度
        delta_psi = abs(total_code % 100 - self.text_sphere.radius * 100) / 100
        
        # 计算平衡度（B值）
        # 基于首三个字符的编码和
        if len(char_codes) >= 3:
            balance_value = (char_codes[0] + char_codes[1] + char_codes[2]) % 10
        else:
            balance_value = 0
        
        return {
            "intersections": intersections,
            "total_char_codes": total_code,
            "avg_char_code": round(avg_code, 2),
            "delta_psi": round(delta_psi, 2),
            "balance_value": balance_value,
            "text_length": len(text),
            "text_sample": text[:100] + "..." if len(text) > 100 else text
        }
    
    def convert_iteration(self) -> Dict:
        """
        执行单次论文转换迭代
        
        返回：
        - Dict: 本次转换的结果
        """
        logger.info(f"[论文转换系统] 开始转换迭代")
        
        # 使用过程之圆处理
        process_result = self.process_circle.process_step(
            input_data=self.processed_content[:50]  # 使用前50字符作为输入
        )
        
        if process_result is None:
            logger.info("[论文转换系统] 达到最大迭代次数，转换结束")
            return None
        
        # 使用球体模型分析文本
        sphere_result = self._process_text_with_sphere(self.processed_content[:1000])
        
        # 使用数据分析尺子进行分析
        analysis_result = self.analysis_ruler.process_step()
        
        # 记录转换历史
        iteration_result = {
            "iteration": self.process_circle.current_iteration,
            "process_result": process_result,
            "sphere_analysis": sphere_result,
            "data_analysis": analysis_result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.conversion_history.append(iteration_result)
        self.sphere_intersections.extend(sphere_result["intersections"])
        
        # 更新处理后的内容（简化实现：添加转换标记）
        self.processed_content = f"[转换迭代{self.process_circle.current_iteration}] {self.processed_content}"
        
        logger.info(f"[论文转换系统] 完成转换迭代 {self.process_circle.current_iteration}")
        return iteration_result
    
    def run_full_conversion(self) -> List[Dict]:
        """
        运行完整的论文转换过程
        
        返回：
        - List[Dict]: 所有转换迭代的结果
        """
        logger.info("[论文转换系统] 开始完整论文转换")
        
        # 验证系统完整性
        try:
            verification_system.verify_integrity()
            logger.info("[论文转换系统] 转换前验证通过")
        except RuntimeError as e:
            logger.error(f"[论文转换系统] 转换前验证失败: {e}")
            raise
        
        # 执行转换循环
        results = []
        while True:
            result = self.convert_iteration()
            if result is None:
                break
            results.append(result)
            time.sleep(0.5)  # 模拟处理时间
        
        # 验证转换后系统完整性
        try:
            verification_system.verify_integrity()
            logger.info("[论文转换系统] 转换后验证通过")
        except RuntimeError as e:
            logger.error(f"[论文转换系统] 转换后验证失败: {e}")
            raise
        
        logger.info("[论文转换系统] 完整论文转换完成")
        return results
    
    def generate_conversion_report(self) -> Dict:
        """
        生成转换报告
        
        返回：
        - Dict: 完整的转换报告
        """
        logger.info("[论文转换系统] 生成转换报告")
        
        # 计算总体统计
        total_intersections = len(self.sphere_intersections)
        avg_delta_psi = sum(r["sphere_analysis"]["delta_psi"] 
                          for r in self.conversion_history) / len(self.conversion_history) if self.conversion_history else 0
        
        report = {
            "论文标题": self.paper_title,
            "原始内容长度": len(self.original_content),
            "处理后内容长度": len(self.processed_content),
            "总转换迭代次数": len(self.conversion_history),
            "总球体相交点": total_intersections,
            "平均违和强度": round(avg_delta_psi, 4),
            "转换历史": self.conversion_history,
            "球体参数": {
                "半径": self.text_sphere.radius,
                "中心点": self.text_sphere.center
            },
            "系统验证状态": "通过",
            "生成时间": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return report
    
    def save_conversion_result(self, output_path: str):
        """
        保存转换结果到文件
        
        参数：
        - output_path: 输出文件路径
        """
        report = self.generate_conversion_report()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logger.info(f"[论文转换系统] 转换结果已保存到: {output_path}")
    
    @staticmethod
    def batch_convert_folder(input_folder: str, output_folder: str, max_iterations: int = 5):
        """
        批量转换文件夹中的所有文件
        
        参数：
        - input_folder: 输入文件夹路径
        - output_folder: 输出文件夹路径
        - max_iterations: 最大转换迭代次数
        """
        logger.info(f"[批量转换] 开始处理文件夹: {input_folder}")
        
        # 确保输出文件夹存在
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            logger.info(f"[批量转换] 创建输出文件夹: {output_folder}")
        
        # 获取输入文件夹中的所有文件
        files = [f for f in os.listdir(input_folder) 
                if os.path.isfile(os.path.join(input_folder, f))]
        
        logger.info(f"[批量转换] 找到 {len(files)} 个文件")
        
        # 处理每个文件
        for file_name in files:
            try:
                file_path = os.path.join(input_folder, file_name)
                logger.info(f"[批量转换] 处理文件: {file_name}")
                
                # 生成输出文件名（保持原文件名，将扩展名改为.json）
                base_name, _ = os.path.splitext(file_name)
                output_file_name = f"{base_name}.json"
                output_path = os.path.join(output_folder, output_file_name)
                
                # 创建转换器并转换
                converter = PaperConverter(paper_title=base_name, max_iterations=max_iterations)
                converter.load_paper_from_file(file_path)
                converter.run_full_conversion()
                converter.save_conversion_result(output_path)
                
                logger.info(f"[批量转换] 文件处理完成: {file_name}")
                
            except Exception as e:
                logger.error(f"[批量转换] 处理文件 {file_name} 时出错: {e}")
                continue
        
        logger.info(f"[批量转换] 文件夹处理完成，共处理 {len(files)} 个文件")

# 示例使用
def demonstrate_paper_conversion():
    """
    演示论文转换系统的使用
    """
    logger.info("=== 论文转换系统演示开始 ===")
    
    # 示例论文内容
    sample_paper = """
    文字穿刺球体模型研究
    
    摘要：本文提出了一种基于球体数学的文字分析模型，称为文字穿刺球体模型。
    该模型将文字映射到三维空间中的球体表面，通过检测文字线段与球体的相交点，
    计算文字的违和强度和认知特征。研究结果表明，该模型能够有效分析文字的认知结构，
    为自然语言处理和认知科学研究提供了新的视角。
    
    关键词：文字分析；球体数学；认知结构；违和强度
    """
    
    # 创建转换系统实例
    converter = PaperConverter(paper_title="文字穿刺球体模型研究", max_iterations=3)
    
    # 加载论文
    converter.load_paper(sample_paper)
    
    # 运行完整转换
    results = converter.run_full_conversion()
    
    # 生成并保存报告
    converter.save_conversion_result("论文转换结果.json")
    
    # 显示结果
    logger.info(f"\n=== 转换结果摘要 ===")
    logger.info(f"总转换迭代次数: {len(results)}")
    logger.info(f"总相交点数量: {len(converter.sphere_intersections)}")
    logger.info(f"原始内容长度: {len(converter.original_content)} 字符")
    logger.info(f"处理后内容长度: {len(converter.processed_content)} 字符")
    
    # 显示自指分析
    analysis = converter.process_circle.analyze_memory()
    logger.info(f"\n=== 自指分析结果 ===")
    logger.info(f"总迭代次数: {analysis['总迭代次数']}")
    logger.info(f"自指引用次数: {len(analysis['自指引用'])}")
    
    logger.info("=== 论文转换系统演示结束 ===")

if __name__ == "__main__":
    import sys
    
    # 验证系统完整性
    try:
        verification_system.verify_integrity()
        logger.info("系统完整性验证通过！")
        
        # 检查命令行参数
        if len(sys.argv) == 3:
            # 批量转换模式
            input_folder = sys.argv[1]
            output_folder = sys.argv[2]
            logger.info(f"启动批量转换模式: {input_folder} -> {output_folder}")
            PaperConverter.batch_convert_folder(input_folder, output_folder)
        else:
            # 默认演示模式
            demonstrate_paper_conversion()
            
    except RuntimeError as e:
        logger.error(f"系统验证失败: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"程序执行错误: {e}")
        exit(1)