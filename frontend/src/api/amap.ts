/**
 * 高德地图API封装
 */
const AMAP_KEY = import.meta.env.VITE_AMAP_KEY;

/**
 * 地点搜索接口
 * @param keyword 搜索关键词
 * @param city 城市名称
 * @returns 搜索结果
 */
export async function searchPlaces(keyword: string, city: string = ''): Promise<any> {
  if (!AMAP_KEY) {
    console.error('请配置高德地图API密钥');
    return { pois: [] };
  }

  const url = new URL('https://restapi.amap.com/v3/place/text');
  url.searchParams.append('key', AMAP_KEY);
  url.searchParams.append('keywords', keyword);
  if (city) {
    url.searchParams.append('city', city);
  }
  url.searchParams.append('output', 'json');

  try {
    const response = await fetch(url.toString());
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('地点搜索失败:', error);
    return { pois: [] };
  }
}

/**
 * 路径规划接口
 * @param origin 起点坐标 (lon,lat)
 * @param destination 终点坐标 (lon,lat)
 * @param mode 交通方式：driving（驾车）、walking（步行）、bicycling（骑行）、transit（公交）
 * @returns 路径规划结果
 */
export async function getRoute(
  origin: string,
  destination: string,
  mode: 'driving' | 'walking' | 'bicycling' | 'transit' = 'driving'
): Promise<any> {
  if (!AMAP_KEY) {
    console.error('请配置高德地图API密钥');
    return null;
  }

  const url = new URL(`https://restapi.amap.com/v3/direction/${mode}`);
  url.searchParams.append('key', AMAP_KEY);
  url.searchParams.append('origin', origin);
  url.searchParams.append('destination', destination);
  url.searchParams.append('output', 'json');

  // 公交换乘需要额外参数
  if (mode === 'transit') {
    url.searchParams.append('city', ''); // 城市名称，空表示自动识别
    url.searchParams.append('cityd', ''); // 目的地城市，空表示自动识别
  }

  try {
    const response = await fetch(url.toString());
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('路径规划失败:', error);
    return null;
  }
}

/**
 * 坐标逆地理编码
 * @param location 坐标 (lon,lat)
 * @returns 地址信息
 */
export async function reverseGeocode(location: string): Promise<any> {
  if (!AMAP_KEY) {
    console.error('请配置高德地图API密钥');
    return null;
  }

  const url = new URL('https://restapi.amap.com/v3/geocode/regeo');
  url.searchParams.append('key', AMAP_KEY);
  url.searchParams.append('location', location);
  url.searchParams.append('output', 'json');

  try {
    const response = await fetch(url.toString());
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('逆地理编码失败:', error);
    return null;
  }
}