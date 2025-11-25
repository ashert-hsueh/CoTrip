/**
 * 旅行本信息
 */
export interface TripNotebook {
  id: string;
  title: string;
  description?: string;
  coverColor: string;
  createdAt: string;
  updatedAt: string;
  // 临时使用 mock 数据，后续会从后端获取
  destinations?: Destination[];
  routes?: Route[];
}

/**
 * 目的地信息
 */
export interface Destination {
  id: string;
  name: string;
  address: string;
  location: string; // 坐标 (lon,lat)
  description?: string;
  type?: string; // 地点类型
  rating?: number; // 评分
}

/**
 * 路线信息
 */
export interface Route {
  id: string;
  origin: string;
  destination: string;
  mode: 'driving' | 'walking' | 'bicycling' | 'transit';
  distance: string; // 距离
  duration: string; // 预计时间
  path: string; // 路线坐标
  steps?: RouteStep[]; // 路线步骤
}

/**
 * 路线步骤
 */
export interface RouteStep {
  instruction: string; // 行驶指示
  distance: string; // 距离
  duration: string; // 时间
  orientation?: string; // 方向
  road?: string; // 道路名称
  action?: string; // 动作
}

/**
 * 交通方式类型
 */
export type TransportationMode = 'driving' | 'walking' | 'bicycling' | 'transit';

/**
 * 交通方式中文名称映射
 */
export const TransportationModeNames: Record<TransportationMode, string> = {
  driving: '驾车',
  walking: '步行',
  bicycling: '骑行',
  transit: '公共交通'
};