<template>
  <el-dialog
    :model-value="visible"
    :title="editingBill ? '编辑账单' : '添加账单'"
    width="600px"
    @close="handleClose"
    @update:model-value="handleModalUpdate"
  >
    <el-form
      ref="formRef"
      :model="formData"
      label-width="100px"
      style="margin-top: 20px;"
    >
      <!-- 账单类型 -->
      <el-form-item
        label="账单类型"
        prop="type"
        :rules="[{ required: true, message: '请选择账单类型', trigger: 'change' }]"
      >
        <el-select v-model="formData.type" placeholder="请选择" style="width: 100%;">
          <el-option
            v-for="type in billTypes"
            :key="type.value"
            :label="type.label"
            :value="type.value"
          >
            <template #default>
              <div style="display: flex; align-items: center; gap: 8px;">
                <div
                  style="width: 12px; height: 12px; border-radius: 50%;"
                  :style="{ background: type.color }"
                ></div>
                {{ type.label }}
              </div>
            </template>
          </el-option>
        </el-select>
      </el-form-item>

      <!-- 货币和金额 -->
      <el-row :gutter="16">
        <el-col :span="8">
          <el-form-item
            label="货币"
            prop="currency"
            :rules="[{ required: true, message: '请选择货币', trigger: 'change' }]"
          >
            <el-select v-model="formData.currency" placeholder="选择货币" style="width: 100%;">
              <el-option label="人民币 (¥)" value="CNY" />
              <el-option label="港币 (HK$)" value="HKD" />
              <el-option label="澳门元 (MOP)" value="MOP" />
              <el-option label="美元 ($)" value="USD" />
              <el-option label="欧元 (€)" value="EUR" />
              <el-option label="英镑 (£)" value="GBP" />
              <el-option label="澳大利亚元 (A$)" value="AUD" />
              <el-option label="日元 (¥)" value="JPY" />
              <el-option label="韩元 (₩)" value="KRW" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="16">
          <el-form-item
            label="金额"
            prop="amount"
            :rules="[
              { required: true, message: '请输入金额', trigger: 'blur' },
              { type: 'number', min: 0.01, message: '金额必须大于0', trigger: 'blur' }
            ]"
          >
            <el-input
              v-model.number="formData.amount"
              :placeholder="`请输入金额 (${getCurrencySymbol(formData.currency || 'CNY')})`"
              type="number"
              step="0.01"
              style="width: 100%;"
            >
              <template #prefix>
                <span style="margin-right: 8px; color: #606266;">
                  {{ getCurrencySymbol(formData.currency || 'CNY') }}
                </span>
              </template>
            </el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 支付账户 -->
      <el-form-item
        label="支付账户"
        prop="payment_account"
        :rules="[{ required: true, message: '请选择支付账户', trigger: 'change' }]"
      >
        <el-select v-model="formData.payment_account" placeholder="请选择支付账户" style="width: 100%;">
          <el-option label="现金" value="cash" />
          <el-option label="支付宝" value="alipay" />
          <el-option label="微信支付" value="wechat" />
          <el-option label="银行卡" value="bank_card" />
          <el-option label="信用卡" value="credit_card" />
        </el-select>
      </el-form-item>

      <!-- 付款人 -->
      <el-form-item
        label="付款人"
        prop="payer_id"
        :rules="[{ required: true, message: '请选择付款人', trigger: 'change' }]"
      >
        <el-select v-model="formData.payer_id" placeholder="请选择" style="width: 100%;">
          <el-option
            v-for="member in members"
            :key="member.id"
            :label="member.username"
            :value="member.id"
          />
        </el-select>
      </el-form-item>

      <!-- 参与者 -->
      <el-form-item
        label="参与者"
        prop="participant_ids"
        :rules="[{ required: true, message: '请选择参与者', trigger: 'change' }]"
      >
        <el-select
          v-model="formData.participant_ids"
          placeholder="请选择参与者（可多选）"
          multiple
          style="width: 100%;"
        >
          <el-option
            v-for="member in members"
            :key="member.id"
            :label="member.username"
            :value="member.id"
          />
        </el-select>
      </el-form-item>

      <!-- 发生时间 -->
      <el-form-item
        label="发生时间"
        prop="occurred_at"
        :rules="[{ required: true, message: '请选择发生时间', trigger: 'change' }]"
      >
        <el-date-picker
          v-model="formData.occurred_at"
          type="datetime"
          placeholder="选择日期时间"
          style="width: 100%;"
          value-format="YYYY-MM-DD HH:mm:ss"
        />
      </el-form-item>

      <!-- 描述 -->
      <el-form-item label="备注">
        <el-input
          v-model="formData.description"
          type="textarea"
          placeholder="添加备注信息（可选）"
          :rows="3"
          maxlength="200"
          show-word-limit
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="closeModal">取消</el-button>
        <el-button
          type="primary"
          @click="handleSubmit"
          :loading="submitting"
          style="background: #FFA939; border-color: #FFA939;"
        >
          {{ editingBill ? '保存修改' : '添加账单' }}
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue';
import { ElMessage } from 'element-plus';
import {
  createBillItem,
  updateBillItem,
  type BillItem,
  type BillItemCreateRequest,
  type BillItemUpdateRequest,
  BILL_TYPES
} from '../api/ledger';
import type { UserSimple } from '../api/ledger';

// Props
const props = defineProps<{
  visible: boolean;
  ledgerId: number;
  members: UserSimple[];
  editingBill?: BillItem;
}>();

// Emits
const emit = defineEmits<{
  'update:visible': [visible: boolean];
  'success': [];
}>();

// Refs
const formRef = ref();
const submitting = ref(false);
const billTypes = ref(BILL_TYPES);

// 表单数据
const formData = ref<(BillItemCreateRequest | BillItemUpdateRequest) & {
  currency?: string;
  payment_account?: string;
}>({
  type: '',
  amount: 0,
  payer_id: 0,
  participant_ids: [],
  description: '',
  occurred_at: new Date().toISOString().slice(0, 19),
  currency: 'CNY',
  payment_account: 'cash'
});

// 获取货币符号
const getCurrencySymbol = (currency: string): string => {
  const symbols: Record<string, string> = {
    CNY: '¥',
    HKD: 'HK$',
    MOP: 'MOP$',
    USD: '$',
    EUR: '€',
    GBP: '£',
    AUD: 'A$',
    JPY: '¥',
    KRW: '₩'
  };
  return symbols[currency] || '¥';
};

// 计算属性：判断是否为编辑模式
const isEditMode = computed(() => !!props.editingBill);

// 监听visible变化，初始化表单
watch(
  () => props.visible,
  (newVal) => {
    if (newVal) {
      if (isEditMode.value && props.editingBill) {
        // 编辑模式：填充现有数据
        formData.value = {
          type: props.editingBill.type,
          amount: props.editingBill.amount / 100, // 分转元
          payer_id: props.editingBill.payer_id,
          participant_ids: props.editingBill.participants.map(p => p.id),
          description: props.editingBill.description || '',
          occurred_at: props.editingBill.occurred_at.slice(0, 19),
          currency: (props.editingBill as any).currency || 'CNY',
          payment_account: (props.editingBill as any).payment_account || 'cash'
        };
      } else {
        // 新增模式：重置表单
        resetForm();
      }
      // 重置表单验证
      setTimeout(() => {
        formRef.value?.clearValidate();
      }, 0);
    }
  }
);

// 监听editingBill变化
watch(
  () => props.editingBill,
  (newBill) => {
    if (newBill && props.visible) {
      // 更新表单数据
      formData.value = {
        type: newBill.type,
        amount: newBill.amount / 100,
        payer_id: newBill.payer_id,
        participant_ids: newBill.participants.map(p => p.id),
        description: newBill.description || '',
        occurred_at: newBill.occurred_at.slice(0, 19),
        currency: (newBill as any).currency || 'CNY',
        payment_account: (newBill as any).payment_account || 'cash'
      };
    }
  },
  { deep: true }
);

// 重置表单
const resetForm = () => {
  formData.value = {
    type: '',
    amount: 0,
    payer_id: 0,
    participant_ids: [],
    description: '',
    occurred_at: new Date().toISOString().slice(0, 19),
    currency: 'CNY',
    payment_account: 'cash'
  };
};

// 关闭模态框
const closeModal = () => {
  resetForm();
  emit('update:visible', false);
};

// 处理模态框更新
const handleModalUpdate = (value: boolean) => {
  if (!value) {
    closeModal();
  }
};

// 处理弹窗关闭
const handleClose = () => {
  closeModal();
};

// 表单验证和提交
const handleSubmit = async () => {
  if (!formRef.value) return;

  try {
    // 表单验证
    await formRef.value.validate();
    submitting.value = true;

    // 转换金额（元转分）
    const amountInCents = Math.round((formData.value.amount || 0) * 100);

    if (isEditMode.value && props.editingBill) {
      // 编辑模式
      const updateData: BillItemUpdateRequest = {
        type: formData.value.type,
        amount: amountInCents,
        payer_id: formData.value.payer_id,
        participant_ids: formData.value.participant_ids,
        description: formData.value.description,
        occurred_at: formData.value.occurred_at
      };

      const response = await updateBillItem(props.editingBill.id, updateData);
      if (response.success) {
        ElMessage.success('账单更新成功');
        emit('success');
        closeModal();
      } else {
        ElMessage.error(response.message || '更新账单失败');
      }
    } else {
      // 新增模式
      const createData: BillItemCreateRequest = {
        type: formData.value.type ?? '',
        amount: amountInCents,
        payer_id: formData.value.payer_id ?? 0,
        participant_ids: formData.value.participant_ids ?? [],
        description: formData.value.description,
        occurred_at: formData.value.occurred_at
      };

      const response = await createBillItem(props.ledgerId, createData);
      if (response.success) {
        ElMessage.success('账单添加成功');
        emit('success');
        closeModal();
      } else {
        ElMessage.error(response.message || '添加账单失败');
      }
    }
  } catch (error: any) {
    if (error.name === 'ValidationError') {
      return; // 表单验证失败，不处理
    }
    console.error('提交账单失败:', error);
    ElMessage.error('网络错误，请稍后重试');
  } finally {
    submitting.value = false;
  }
};
</script>

<style scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* 修复标签和输入框的对齐 */
:deep(.el-form-item__label) {
  padding-right: 12px;
}

/* 货币和金额行布局优化 */
:deep(.el-row) {
  margin-bottom: 20px;
}

:deep(.el-col) {
  display: flex;
  align-items: flex-start;
}

/* 当货币改变时，金额输入框的符号也会相应变化 */
:deep(.el-input__prefix) {
  color: #606266;
  font-size: 14px;
}

/* 优化多选框样式 */
:deep(.el-select__tags) {
  flex-wrap: wrap;
}

:deep(.el-select__tags-text) {
  margin-bottom: 4px;
}
</style>
