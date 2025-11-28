<template>
  <div class="ledger-list-container">
    <!-- 页面标题和操作区 -->
    <div class="page-header">
      <h1 class="page-title">我的账本</h1>
      <el-button type="primary" @click="showCreateModal = true" style="background: #FFA939; border-color: #FFA939;">
        <el-icon><Plus /></el-icon>
        创建账本
      </el-button>
    </div>

    <!-- 账本列表 -->
    <div class="ledgers-grid">
      <div
        v-for="ledger in ledgers"
        :key="ledger.id"
        class="ledger-card"
        @click="goToLedgerDetail(ledger.id)"
      >
        <div class="card-header">
          <h3 class="card-title">{{ ledger.title }}</h3>
          <div class="card-actions">
            <el-button
              text
              size="small"
              @click.stop="deleteLedger(ledger.id)"
              type="danger"
            >
              <el-icon><Delete /></el-icon>
            </el-button>
          </div>
        </div>

        <div class="card-content">
          <div class="card-stats">
            <div class="stat-item">
              <span class="stat-label">成员</span>
              <span class="stat-value">{{ ledger.member_count }}人</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">总支出</span>
              <span class="stat-value" style="color: #FF6B6B;">¥{{ formatAmount(ledger.total_amount) }}</span>
            </div>
          </div>

          <div class="card-meta">
            <span class="meta-item">
              <el-icon size="14"><Clock /></el-icon>
              {{ formatDate(ledger.created_at) }}
            </span>
          </div>
        </div>

        <div class="card-footer">
          <el-button text size="small">查看详情 <el-icon><ArrowRight /></el-icon></el-button>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="ledgers.length === 0 && !loading" class="empty-state">
      <el-empty
        description="还没有创建任何账本"
        :image-size="120"
      >
        <template #image>
          <div style="width: 120px; height: 120px; background: #F9F3EE; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
            <el-icon size="60" style="color: #FFA939;"><Wallet /></el-icon>
          </div>
        </template>
        <template #description>
          <span style="color: #666;">创建第一个账本，开始记录旅行开销吧</span>
        </template>
        <el-button type="primary" @click="showCreateModal = true" style="background: #FFA939; border-color: #FFA939;">
          <el-icon><Plus /></el-icon>
          创建账本
        </el-button>
      </el-empty>
    </div>

    <!-- 创建账本弹窗 -->
    <el-dialog
      v-model="showCreateModal"
      title="创建新账本"
      width="500px"
      @close="resetCreateForm"
    >
      <el-form
        ref="createFormRef"
        :model="createForm"
        label-width="100px"
        style="margin-top: 20px;"
      >
        <el-form-item
          label="账本名称"
          prop="title"
          :rules="[{ required: true, message: '请输入账本名称', trigger: 'blur' }]"
        >
          <el-input
            v-model="createForm.title"
            placeholder="例如：三亚旅行账本"
            maxlength="50"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="旅行计划">
          <el-select
            v-model="createForm.travel_plan_id"
            placeholder="可选：关联到已有的旅行计划"
            style="width: 100%;"
          >
            <el-option label="暂无旅行计划" value="" />
            <!-- TODO: 从API获取旅行计划列表 -->
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreateModal = false">取消</el-button>
          <el-button
            type="primary"
            @click="handleCreateLedger"
            :loading="creating"
            style="background: #FFA939; border-color: #FFA939;"
          >
            创建
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus, Delete, Clock, Wallet, ArrowRight } from '@element-plus/icons-vue';
import {
  getMyLedgers,
  createLedger,
  deleteLedger as deleteLedgerApi,
  Ledger,
  LedgerCreateRequest,
  formatAmount,
  formatDate
} from '../api/ledger';

const router = useRouter();
const createFormRef = ref();

// 状态管理
const ledgers = ref<Ledger[]>([]);
const loading = ref(true);
const creating = ref(false);
const showCreateModal = ref(false);

// 表单数据
const createForm = ref<LedgerCreateRequest>({
  title: '',
  travel_plan_id: undefined
});

// 获取账本列表
const fetchLedgers = async () => {
  try {
    loading.value = true;
    const response = await getMyLedgers();
    if (response.success && response.data) {
      ledgers.value = response.data;
    } else {
      ElMessage.error(response.message || '获取账本列表失败');
    }
  } catch (error) {
    console.error('获取账本列表失败:', error);
    ElMessage.error('网络错误，请稍后重试');
  } finally {
    loading.value = false;
  }
};

// 前往账本详情
const goToLedgerDetail = (ledgerId: number) => {
  router.push(`/ledgers/${ledgerId}`);
};

// 创建账本
const handleCreateLedger = async () => {
  if (!createFormRef.value) return;

  try {
    await createFormRef.value.validate();
    creating.value = true;

    const response = await createLedger(createForm.value);
    if (response.success) {
      ElMessage.success(response.message);
      showCreateModal.value = false;
      fetchLedgers();
    } else {
      ElMessage.error(response.message || '创建账本失败');
    }
  } catch (error: any) {
    if (error.name === 'ValidationError') {
      return; // 表单验证失败，不处理
    }
    console.error('创建账本失败:', error);
    ElMessage.error('网络错误，请稍后重试');
  } finally {
    creating.value = false;
  }
};

// 删除账本
const deleteLedger = async (ledgerId: number) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这个账本吗？删除后将无法恢复，且会删除所有相关账单。',
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    );

    const response = await deleteLedgerApi(ledgerId);
    if (response.success) {
      ElMessage.success(response.message);
      fetchLedgers();
    } else {
      ElMessage.error(response.message || '删除账本失败');
    }
  } catch (error: any) {
    if (error.name === 'ElMessageBoxCancel') {
      return; // 用户取消删除
    }
    console.error('删除账本失败:', error);
    ElMessage.error('网络错误，请稍后重试');
  }
};

// 重置创建表单
const resetCreateForm = () => {
  createForm.value = {
    title: '',
    travel_plan_id: undefined
  };
  createFormRef.value?.resetFields();
};

// 页面加载时获取数据
onMounted(() => {
  fetchLedgers();
});
</script>

<style scoped>
.ledger-list-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
  min-height: 100vh;
  background: #F9F3EE;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

/* 账本卡片样式 */
.ledgers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.ledger-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.ledger-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  border-color: #FFA939;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0;
  flex: 1;
  margin-right: 12px;
  line-height: 1.4;
}

.card-actions {
  display: flex;
  gap: 8px;
}

.card-content {
  margin-bottom: 16px;
}

.card-stats {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-label {
  font-size: 12px;
  color: #999;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #666;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.card-footer {
  display: flex;
  justify-content: flex-end;
}

/* 空状态样式 */
.empty-state {
  margin-top: 60px;
  text-align: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .ledger-list-container {
    padding: 16px;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .ledgers-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}
</style>
