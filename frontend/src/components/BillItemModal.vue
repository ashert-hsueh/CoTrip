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

      <!-- 金额 -->
      <el-form-item
        label="金额"
        prop="amount"
        :rules="[
          { required: true, message: '请输入金额', trigger: 'blur' },
          { type: 'number', min: 1, message: '金额必须大于0', trigger: 'blur' }
        ]"
      >
        <el-input
          v-model.number="formData.amount"
          placeholder="请输入金额（元）"
          prefix-icon="¥"
          type="number"
          step="0.01"
          style="width: 100%;"
        />
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
const formData = ref<BillItemCreateRequest | BillItemUpdateRequest>({
  type: '',
  amount: 0,
  payer_id: 0,
  participant_ids: [],
  description: '',
  occurred_at: new Date().toISOString().slice(0, 19)
});

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
          occurred_at: props.editingBill.occurred_at.slice(0, 19)
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
        occurred_at: newBill.occurred_at.slice(0, 19)
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
    occurred_at: new Date().toISOString().slice(0, 19)
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

/* 优化多选框样式 */
:deep(.el-select__tags) {
  flex-wrap: wrap;
}

:deep(.el-select__tags-text) {
  margin-bottom: 4px;
}
</style>
