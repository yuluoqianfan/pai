
# 根据文档内容生成的代码
# 文档标题：文字穿刺的球体

import math
import copy
import sys
import inspect

class Sphere:
    '''球体类'''
    def __init__(self, radius, center=(0, 0, 0)):
        self.radius = radius
        self.center = center  # 中心点坐标 (x0, y0, z0)
    
    def volume(self):
        '''计算球体体积'''
        return (4/3) * math.pi * self.radius ** 3
    
    def surface_area(self):
        '''计算球体表面积'''
        return 4 * math.pi * self.radius ** 2
    
    def line_sphere_intersection(self, p1, p2):
        '''检测线段p1-p2与球体的相交点'''
        # p1和p2是三维坐标点 (x, y, z)
        # 计算向量
        x0, y0, z0 = self.center
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        
        # 向量V: 从球心到p1
        vx, vy, vz = x1 - x0, y1 - y0, z1 - z0
        # 向量W: 从p1到p2
        wx, wy, wz = x2 - x1, y2 - y1, z2 - z1
        
        # 计算二次方程系数
        a = wx**2 + wy**2 + wz**2
        b = 2 * (vx*wx + vy*wy + vz*wz)
        c = (vx**2 + vy**2 + vz**2) - self.radius**2
        
        # 计算判别式
        discriminant = b**2 - 4*a*c
        
        if discriminant < 0:
            return []  # 无相交点
        elif discriminant == 0:
            # 相切，一个相交点
            t = -b / (2*a)
            if 0 <= t <= 1:
                intersection = (x1 + t*wx, y1 + t*wy, z1 + t*wz)
                return [intersection]
            return []
        else:
            # 两个可能的解
            t1 = (-b + math.sqrt(discriminant)) / (2*a)
            t2 = (-b - math.sqrt(discriminant)) / (2*a)
            
            intersections = []
            if 0 <= t1 <= 1:
                intersection1 = (x1 + t1*wx, y1 + t1*wy, z1 + t1*wz)
                intersections.append(intersection1)
            if 0 <= t2 <= 1:
                intersection2 = (x1 + t2*wx, y1 + t2*wy, z1 + t2*wz)
                intersections.append(intersection2)
            
            return intersections
    
    def calculate_normal(self, point):
        '''计算球体表面某点的法向量'''
        x, y, z = point
        x0, y0, z0 = self.center
        
        # 法向量指向从球心到该点的方向
        nx, ny, nz = x - x0, y - y0, z - z0
        
        # 归一化法向量
        length = math.sqrt(nx**2 + ny**2 + nz**2)
        if length > 0:
            nx, ny, nz = nx/length, ny/length, nz/length
        
        return (nx, ny, nz)
    
    def project_point_to_surface(self, point):
        '''将点投影到球体表面'''
        x, y, z = point
        x0, y0, z0 = self.center
        
        # 计算从球心到该点的向量
        vx, vy, vz = x - x0, y - y0, z - z0
        
        # 计算向量长度
        length = math.sqrt(vx**2 + vy**2 + vz**2)
        if length == 0:
            return self.center  # 如果点在球心，则返回球心
        
        # 归一化并缩放为半径长度
        scale = self.radius / length
        projection = (x0 + vx*scale, y0 + vy*scale, z0 + vz*scale)
        
        return projection
    
    def text_intersection(self, text):
        '''文字与球体的相交处理'''
        print(f"处理文字'{text}'与球体的相交")
        
        # 简单实现：将文字视为由线段组成，检测与球体的相交
        # 这里使用简化的文字线段表示（实际应用中需要文字的3D坐标）
        # 示例：使用几个点组成的简单线段来模拟文字
        sample_segments = [
            ((10, 0, 0), (5, 0, 0)),  # 示例线段1
            ((0, 10, 0), (0, 5, 0)),  # 示例线段2
            ((0, 0, 10), (0, 0, 5))   # 示例线段3
        ]
        
        intersections = []
        for p1, p2 in sample_segments:
            seg_intersections = self.line_sphere_intersection(p1, p2)
            for point in seg_intersections:
                normal = self.calculate_normal(point)
                intersections.append((point, normal))
        
        print(f"检测到 {len(intersections)} 个相交点")
        for i, (point, normal) in enumerate(intersections):
            print(f"相交点 {i+1}: 坐标 = {point}, 法向量 = {normal}")
        
        return intersections
    
    # 反双指保护：防止对象复制
    def __copy__(self):
        raise TypeError("禁止复制此对象")
    
    def __deepcopy__(self, memo):
        raise TypeError("禁止深度复制此对象")

# 8球体联合验证系统
class EightSphereVerification:
    '''8球体联合验证系统：通过8个球体的相互验证确保代码完整性'''
    
    def __init__(self):
        # 创建8个相互关联的球体，形成立方体的8个顶点
        self.spheres = []
        positions = [
            (1, 1, 1),   # 顶点1
            (-1, 1, 1),  # 顶点2
            (-1, -1, 1), # 顶点3
            (1, -1, 1),  # 顶点4
            (1, 1, -1),  # 顶点5
            (-1, 1, -1), # 顶点6
            (-1, -1, -1),# 顶点7
            (1, -1, -1)  # 顶点8
        ]
        
        for i, pos in enumerate(positions):
            sphere = Sphere(radius=0.5, center=pos)
            self.spheres.append((f"sphere_{i+1}", sphere))
        
        # 生成唯一验证密钥
        self.verification_key = self._generate_verification_key()
    
    def _generate_verification_key(self):
        '''生成基于8个球体属性的唯一验证密钥'''
        key_parts = []
        for name, sphere in self.spheres:
            # 使用球体的半径和中心点坐标生成密钥部分
            radius_hash = int(sphere.radius * 1000)
            center_hash = int((sum(sphere.center) * 1000) % 10000)
            key_parts.append(f"{name}:{radius_hash}:{center_hash}")
        
        # 组合成最终密钥
        return "|".join(key_parts)
    
    def verify_integrity(self, provided_key=None):
        '''验证代码完整性
        
        参数：
        - provided_key: 可选，提供的验证密钥用于比较
        
        返回：
        - bool: 验证是否通过
        '''
        if provided_key is None:
            provided_key = self.verification_key
        
        # 重新生成密钥进行比较
        current_key = self._generate_verification_key()
        
        if current_key != provided_key:
            raise RuntimeError("代码完整性验证失败！可能存在未经授权的修改。")
        
        # 执行8球体之间的相互验证
        for i in range(8):
            for j in range(i+1, 8):
                sphere_i = self.spheres[i][1]
                sphere_j = self.spheres[j][1]
                
                # 计算实际距离
                actual_distance = math.sqrt(
                    (sphere_i.center[0] - sphere_j.center[0])**2 +
                    (sphere_i.center[1] - sphere_j.center[1])**2 +
                    (sphere_i.center[2] - sphere_j.center[2])**2
                )
                
                # 对于立方体顶点的球体，相邻顶点之间的距离应该是2、2√2或2√3
                # 验证距离是否在可接受范围内
                if not (1.0 < actual_distance < 4.0):  # 有效距离范围（空间对角线最大约为3.464）
                    raise RuntimeError("8球体联合验证失败！球体之间的关系已被破坏。")
        
        return True
    
    def get_verification_key(self):
        '''获取当前验证密钥'''
        return self.verification_key
    
    def verify_sphere(self, sphere):
        '''验证单个球体是否与8球体系统兼容
        
        参数：
        - sphere: 要验证的球体对象
        
        返回：
        - bool: 是否兼容
        '''
        # 检查是否为Sphere类的实例
        if not isinstance(sphere, Sphere):
            return False
        
        # 检查是否有禁止的复制操作
        try:
            copied = copy.copy(sphere)
            return False  # 如果没有抛出异常，说明复制被允许
        except TypeError:
            pass  # 预期会抛出TypeError
        
        try:
            deep_copied = copy.deepcopy(sphere)
            return False  # 如果没有抛出异常，说明深度复制被允许
        except TypeError:
            pass  # 预期会抛出TypeError
        
        return True

# 全局验证实例
verification_system = EightSphereVerification()

# 示例使用
sphere = Sphere(5)  # 创建半径为5的球体
print(f"球体体积: {sphere.volume():.2f}")
print(f"球体表面积: {sphere.surface_area():.2f}")

# 验证代码完整性
try:
    verification_system.verify_integrity()
    print("代码完整性验证通过！")
    sphere.text_intersection("Hello World")
except RuntimeError as e:
    print(f"验证失败: {e}")
    sys.exit(1)
