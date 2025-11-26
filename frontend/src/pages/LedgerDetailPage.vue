<template>
  <div class="ledger-detail-container">
    <!-- 页面头部 -->
    <div class="page-header" style="background: linear-gradient(135deg, #FFA939 0%, #FFC168 100%); color: white;">
      <div class="header-content">
        <div class="header-main">
          <div class="title-section">
            <h1 class="page-title" v-if="!editingTitle">{{ ledgerDetail?.title }}</h1>
            <el-input
              v-else
              v-model="editTitleForm.title"
              size="large"
              placeholder="请输入账本名称"
              @blur="cancelEditTitle"
              @keyup.enter="saveTitle"
              @keyup.esc="cancelEditTitle"
              ref="titleInputRef"
              style="width: 300px;"
            />
          </div>
          <div class="header-actions">
            <el-button
              text
              size="large"
              @click="toggleEditTitle"
              v-if="!editingTitle"
              style="color: white; border-color: white;"
            >
              <el-icon><Edit /></el-icon>
              编辑名称
            </el-button>
            <el-button
              text
              size="large"
              @click="showAddMemberModal = true"
              style="color: white; border-color: white;"
            >
              <el-icon><Plus /></el-icon>
              添加成员
            </el-button>
            <el-button
              type="primary"
              size="large"
              @click="showBillModal = true"
              style="background: white; color: #FFA939; border-color: white;"
            >
              <el-icon><Plus /></el-icon>
              添加账单
            </el-button>
          </div>
        </div>

        <!-- 统计信息 -->
        <div class="stats-section">
          <div class="stat-card">
            <div class="stat-icon" style="background: rgba(255, 255, 255, 0.2);">
              <el-icon size="24"><Wallet /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-label">总支出</span>
              <span class="stat-value">¥{{ formatAmount(ledgerDetail?.total_amount || 0) }}</span>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon" style="background: rgba(255, 255, 255, 0.2);">
              <el-icon size="24"><User /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-label">成员数量</span>
              <span class="stat-value">{{ ledgerDetail?.member_count || 0 }}人</span>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon" style="background: rgba(255, 255, 255, 0.2);">
              <el-icon size="24"><Document /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-label">账单数量</span>
              <span class="stat-value">{{ ledgerDetail?.bill_items?.length || 0 }}笔</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="main-content">
      <div class="content-wrapper">
        <!-- 成员管理 -->
        <div class="panel">
          <div class="panel-header">
            <h2 class="panel-title">成员管理</h2>
          </div>
          <div class="panel-body">
            <div class="members-grid">
              <div
                v-for="member in ledgerDetail?.members || []"
                :key="member.id"
                class="member-card"
              >
                <div class="member-avatar">
                  {{ member.username.charAt(0).toUpperCase() }}
                </div>
                <div class="member-info">
                  <div class="member-name">{{ member.username }}</div>
                  <div class="member-email">{{ member.email }}</div>
                  <div class="member-role" v-if="member.id === ledgerDetail?.creator_id">
                    <el-tag size="small" style="background: #70CDE5; color: white;">创建者</el-tag>
                  </div>
                </div>
                <div class="member-actions" v-if="canManageMembers && member.id !== ledgerDetail?.creator_id">
                  <el-button
                    text
                    size="small"
                    type="danger"
                    @click="removeMember(member.id)"
                  >
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 账单列表 -->
        <div class="panel">
          <div class="panel-header">
            <h2 class="panel-title">账单明细</h2>
            <div class="panel-actions">
              <el-select
                v-model="filterType"
                placeholder="筛选类型"
                size="small"
                style="width: 120px;"
              >
                <el-option label="全部" value="" />
                <el-option
                  v-for="type in billTypes"
                  :key="type.value"
                  :label="type.label"
                  :value="type.value"
                >
                  <template #default>
                    <div style="display: flex; align-items: center; gap: 6px;">
                      <div
                        style="width: 8px; height: 8px; border-radius: 50%;"
                        :style="{ background: type.color }"
                      ></div>
                      {{ type.label }}
                    </div>
                  </template>
                </el-option>
              </el-select>
            </div>
          </div>
          <div class="panel-body">
            <div v-if="filteredBills.length === 0" class="empty-bills">
              <el-empty
                description="还没有添加任何账单"
                :image-size="80"
              >
                <template #description>
                  <span style="color: #666;">添加第一笔账单记录吧</span>
                </template>
              </el-empty>
            </div>

            <el-timeline v-else>
              <el-timeline-item
                v-for="bill in filteredBills"
                :key="bill.id"
                :color="getBillTypeColor(bill.type)"
              >
                <template #dot>
                  <el-icon><Money /></el-icon>
                </template>
                <div class="bill-card">
                  <div class="bill-header">
                    <div class="bill-type-info">
                      <span
                        class="bill-type-badge"
                        :style="{ background: getBillTypeColor(bill.type) }"
                      >
                        {{ getBillTypeLabel(bill.type) }}
                      </span>
                      <span class="bill-amount" style="color: #FF6B6B;">
                        ¥{{ formatAmount(bill.amount) }}
                      </span>
                    </div>
                    <div class="bill-actions">
                      <el-button
                        text
                        size="small"
                        @click="editBill(bill)"
                      >
                        <el-icon><Edit /></el-icon>
                      </el-button>
                      <el-button
                        text
                        size="small"
                        type="danger"
                        @click="deleteBill(bill.id)"
                      >
                        <el-icon><Delete /></el-icon>
                      </el-button>
                    </div>
                  </div>

                  <div class="bill-content">
                    <div class="bill-participants">
                      <span class="payer-info">
                        <el-icon size="14"><User /></el-icon>
                        {{ bill.payer_name }} 支付
                      </span>
                      <span class="split-info">
                        <el-icon size="14"><Divide /></el-icon>
                        参与 {{ bill.participants.length }} 人
                      </span>
                    </div>

                    <div class="bill-description" v-if="bill.description">
                      <el-icon size="14"><Comment /></el-icon>
                      {{ bill.description }}
                    </div>

                    <div class="bill-time">
                      <el-icon size="14"><Clock /></el-icon>
                      {{ formatDate(bill.occurred_at) }}
                    </div>
                  </div>
                </div>
              </el-timeline-item>
            </el-timeline>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加成员弹窗 -->
    <el-dialog
      v-model="showAddMemberModal"
      title="添加成员"
      width="500px"
      @close="resetAddMemberForm"
    >
      <el-form
        ref="addMemberFormRef"
        :model="addMemberForm"
        label-width="100px"
        style="margin-top: 20px;"
      >
        <el-form-item
          label="用户邮箱"
          prop="user_email"
          :rules="[{ required: true, message: '请输入用户邮箱', trigger: 'blur' }]"
        >
          <el-input
            v-model="addMemberForm.user_email"
            placeholder="请输入要添加的成员邮箱"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddMemberModal = false">取消</el-button>
          <el-button
            type="primary"
            @click="handleAddMember"
            :loading="addingMember"
            style="background: #FFA939; border-color: #FFA939;"
          >
            添加
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 账单弹窗 -->
    <BillItemModal
      v-model:visible="showBillModal"
      :ledger-id="ledgerId"
      :members="ledgerDetail?.members || []"
      :editing-bill="currentEditingBill"
      @success="fetchLedgerDetail"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import {
  Edit,
  Plus,
  Delete,
  Wallet,
  User,
  Document,
  Money,
  Divide,
  Comment,
  Clock
} from '@element-plus/icons-vue';
import {
  getLedgerDetail,
  updateLedger,
  addMemberToLedger,
  removeMemberFromLedger,
  deleteBillItem,
  LedgerDetail,
  LedgerUpdateRequest,
  BILL_TYPES,
  formatAmount,
  formatDate
} from '../api/ledger';
import BillItemModal from '../components/BillItemModal.vue';
import type { BillItem } from '../api/ledger';

const route = useRoute();
const titleInputRef = ref();
const addMemberFormRef = ref();

// 路由参数
const ledgerId = computed(() => parseInt(route.params.id as string));

// 状态管理
const loading = ref(true);
const ledgerDetail = ref<LedgerDetail | null>(null);
const editingTitle = ref(false);
const showAddMemberModal = ref(false);
const showBillModal = ref(false);
const addingMember = ref(false);
const currentEditingBill = ref<BillItem | undefined>();
const filterType = ref('');

// 表单数据
const editTitleForm = ref({
  title: ''
});

const addMemberForm = ref({
  user_email: ''
});

// 计算属性
const canManageMembers = computed(() => {
  // TODO: 根据当前登录用户ID和账本创建者ID判断
  // 暂时返回true，实际项目中需要从认证信息中获取当前用户ID
  return true;
});

const filteredBills = computed(() => {
  if (!ledgerDetail.value?.bill_items) return [];

  if (!filterType.value) {
    return ledgerDetail.value.bill_items;
  }

  return ledgerDetail.value.bill_items.filter(bill => bill.type === filterType.value);
});

const billTypes = ref(BILL_TYPES);

// 获取账本详情
const fetchLedgerDetail = async () => {
  try {
    loading.value = true;
    const response = await getLedgerDetail(ledgerId.value);
    if (response.success && response.data) {
      ledgerDetail.value = response.data;
    } else {
      ElMessage.error(response.message || '获取账本详情失败');
    }
  } catch (error) {
    console.error('获取账本详情失败:', error);
    ElMessage.error('网络错误，请稍后重试');
  } finally {
    loading.value = false;
  }
};

// 切换编辑标题模式
const toggleEditTitle = () => {
  if (ledgerDetail.value) {
    editingTitle.value = true;
    editTitleForm.value.title = ledgerDetail.value.title;
    nextTick(() => {
      titleInputRef.value?.$el.querySelector('input')?.focus();
    });
  }
};

// 保存标题
const saveTitle = async () => {
  if (!editTitleForm.value.title.trim()) {
    ElMessage.error('账本名称不能为空');
    return;
  }

  try {
    const updateData: LedgerUpdateRequest = {
      title: editTitleForm.value.title.trim()
    };

    const response = await updateLedger(ledgerId.value, updateData);
    if (response.success) {
      ElMessage.success('账本名称更新成功');
      editingTitle.value = false;
      fetchLedgerDetail();
    } else {
      ElMessage.error(response.message || '更新账本名称失败');
    }
  } catch (error) {
    console.error('更新账本名称失败:', error);
    ElMessage.error('网络错误，请稍后重试');
  }
};

// 取消编辑标题
const cancelEditTitle = () => {
  editingTitle.value = false;
  editTitleForm.value.title = ledgerDetail.value?.title || '';
};

// 添加成员
const handleAddMember = async () => {
  if (!addMemberFormRef.value) return;

  try {
    await addMemberFormRef.value.validate();
    addingMember.value = true;

    // TODO: 根据邮箱查找用户ID（需要实现用户搜索API）
    // 暂时使用固定ID 2，实际项目中需要替换为真实的用户搜索逻辑
    const userId = 2;

    const response = await addMemberToLedger(ledgerId.value, { user_id: userId });
    if (response.success) {
      ElMessage.success('成员添加成功');
      showAddMemberModal.value = false;
      fetchLedgerDetail();
    } else {
      ElMessage.error(response.message || '添加成员失败');
    }
  } catch (error: any) {
    if (error.name === 'ValidationError') {
      return;
    }
    console.error('添加成员失败:', error);
    ElMessage.error('网络错误，请稍后重试');
  } finally {
    addingMember.value = false;
  }
};

// 移除成员
const removeMember = async (userId: number) => {
  try {
    await ElMessageBox.confirm(
      '确定要移除这个成员吗？',
      '移除确认',
      {
        confirmButtonText: '确定移除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    );

    const response = await removeMemberFromLedger(ledgerId.value, userId);
    if (response.success) {
      ElMessage.success('成员移除成功');
      fetchLedgerDetail();
    } else {
      ElMessage.error(response.message || '移除成员失败');
    }
  } catch (error: any) {
    if (error.name === 'ElMessageBoxCancel') {
      return;
    }
    console.error('移除成员失败:', error);
    ElMessage.error('网络错误，请稍后重试');
  }
};

// 编辑账单
const editBill = (bill: BillItem) => {
  currentEditingBill.value = bill;
  showBillModal.value = true;
};

// 删除账单
const deleteBill = async (billItemId: number) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这张账单吗？删除后将无法恢复。',
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    );

    const response = await deleteBillItem(billItemId);
    if (response.success) {
      ElMessage.success('账单删除成功');
      fetchLedgerDetail();
    } else {
      ElMessage.error(response.message || '删除账单失败');
    }
  } catch (error: any) {
    if (error.name === 'ElMessageBoxCancel') {
      return;
    }
    console.error('删除账单失败:', error);
    ElMessage.error('网络错误，请稍后重试');
  }
};

// 重置添加成员表单
const resetAddMemberForm = () => {
  addMemberForm.value = {
    user_email: ''
  };
  addMemberFormRef.value?.resetFields();
};

// 获取账单类型颜色
const getBillTypeColor = (type: string) => {
  const billType = billTypes.value.find(t => t.value === type);
  return billType?.color || '#999';
};

// 获取账单类型标签
const getBillTypeLabel = (type: string) => {
  const billType = billTypes.value.find(t => t.value === type);
  return billType?.label || type;
};

// 监听路由变化
watch(
  () => route.params.id,
  () => {
    fetchLedgerDetail();
  }
);

// 页面加载时获取数据
onMounted(() => {
  fetchLedgerDetail();
});
</script>

<style scoped>
.ledger-detail-container {
  min-height: 100vh;
  background: #F9F3EE;
}

/* 页面头部样式 */
.page-header {
  padding: 40px 0;
  margin-bottom: 32px;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.header-main {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.title-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-title {
  font-size: 32px;
  font-weight: 600;
  margin: 0;
  color: white;
}

.header-actions {
  display: flex;
  gap: 12px;
}

/* 统计信息样式 */
.stats-section {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  background: rgba(255, 255, 255, 0.15);
  padding: 20px 24px;
  border-radius: 12px;
  backdrop-filter: blur(10px);
  min-width: 200px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 4px;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: white;
}

/* 主要内容区域 */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px 48px;
}

.content-wrapper {
  display: grid;
  gap: 24px;
}

/* 面板样式 */
.panel {
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #f0f0f0;
}

.panel-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.panel-actions {
  display: flex;
  gap: 12px;
}

.panel-body {
  padding: 24px;
}

/* 成员管理样式 */
.members-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.member-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 12px;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.member-card:hover {
  border-color: #FFA939;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.member-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FFA939, #FFC168);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 18px;
}

.member-info {
  flex: 1;
  min-width: 0;
}

.member-name {
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.member-email {
  font-size: 12px;
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.member-role {
  margin-top: 4px;
}

.member-actions {
  display: flex;
  gap: 8px;
}

/* 账单样式 */
.empty-bills {
  text-align: center;
  padding: 48px 0;
}

.bill-card {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid #e9ecef;
}

.bill-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.bill-type-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.bill-type-badge {
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.bill-amount {
  font-size: 20px;
  font-weight: 600;
}

.bill-actions {
  display: flex;
  gap: 4px;
}

.bill-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.bill-participants {
  display: flex;
  gap: 16px;
  font-size: 14px;
  color: #666;
}

.payer-info,
.split-info {
  display: flex;
  align-items: center;
  gap: 4px;
}

.bill-description {
  font-size: 14px;
  color: #333;
  display: flex;
  align-items: center;
  gap: 4px;
}

.bill-time {
  font-size: 12px;
  color: #999;
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 4px;
}

/* 时间线样式 */
:deep(.el-timeline) {
  padding: 0;
}

:deep(.el-timeline-item) {
  padding-bottom: 24px;
}

:deep(.el-timeline-item__tail) {
  left: 7px;
  width: 2px;
}

:deep(.el-timeline-item__dot) {
  left: 0;
  width: 16px;
  height: 16px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-header {
    padding: 24px 0;
  }

  .header-content {
    padding: 0 16px;
  }

  .header-main {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .page-title {
    font-size: 24px;
  }

  .header-actions {
    width: 100%;
    justify-content: space-between;
  }

  .stats-section {
    flex-direction: column;
    gap: 16px;
  }

  .stat-card {
    width: 100%;
    min-width: auto;
  }

  .main-content {
    padding: 0 16px 32px;
  }

  .members-grid {
    grid-template-columns: 1fr;
  }

  .panel-body {
    padding: 16px;
  }

  .bill-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .bill-participants {
    flex-direction: column;
    gap: 8px;
  }
}
</style>
