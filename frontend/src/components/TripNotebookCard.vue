<template>
  <div
    class="trip-notebook-card"
    :style="{ backgroundColor: notebook.coverColor }"
    @click="handleClick"
  >
    <div class="notebook-cover">
      <h3 class="notebook-title">{{ notebook.title }}</h3>
      <p class="notebook-date">{{ formattedDate }}</p>
      <div v-if="notebook.destinations?.length" class="notebook-stats">
        <span>{{ notebook.destinations.length }}个目的地</span>
      </div>
    </div>
    <div class="notebook-corner"></div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { TripNotebook } from '../types/trip';

interface Props {
  notebook: TripNotebook;
}

interface Emits {
  (e: 'click', notebook: TripNotebook): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const formattedDate = computed(() => {
  const date = new Date(props.notebook.createdAt);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
});

const handleClick = () => {
  emit('click', props.notebook);
};
</script>

<style scoped>
.trip-notebook-card {
  position: relative;
  width: 220px;
  height: 300px;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  transform: rotate(-2deg);
  margin: 20px;
}

.trip-notebook-card:hover {
  transform: translateY(-8px) rotate(0deg);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.notebook-cover {
  width: 100%;
  height: 100%;
  padding: 30px 20px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  text-align: center;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  position: relative;
  z-index: 1;
}

.notebook-title {
  font-family: '华文行楷', serif;
  font-size: 28px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.95);
  margin-bottom: 20px;
  line-height: 1.3;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.notebook-date {
  font-family: 'Butler', sans-serif;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.85);
  margin-bottom: 10px;
  font-style: italic;
}

.notebook-stats {
  font-family: 'Butler', sans-serif;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.8);
  background: rgba(255, 255, 255, 0.2);
  padding: 4px 12px;
  border-radius: 12px;
  margin-top: auto;
}

.notebook-corner {
  position: absolute;
  top: 0;
  right: 0;
  width: 0;
  height: 0;
  border-top: 40px solid rgba(255, 255, 255, 0.2);
  border-left: 40px solid transparent;
  z-index: 0;
}

/* 添加翻页动画的样式 */
@keyframes flipOpen {
  0% {
    transform: rotateY(0deg);
  }
  50% {
    transform: rotateY(90deg);
  }
  100% {
    transform: rotateY(0deg);
  }
}

.trip-notebook-card.flip-animation {
  animation: flipOpen 0.6s ease;
}
</style>