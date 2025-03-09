<script setup>
import StatusRow from '@/components/StatusRow.vue';
import SubCategoryRow from '@/components/SubCategoryRow.vue';
import TypeRow from '@/components/TypeRow.vue';
import CategoryRow from '@/components/CategoryRow.vue';
import AddTransRow from '@/components/AddTransRow.vue';
</script>

<template>
  <div class="container">
    <StatusRow />
    <TypeRow />
    <CategoryRow />
    <SubCategoryRow />
    <AddTransRow />
  </div>
</template>

<!-- Подключаем стили -->
<style>
@import '@/assets/addview.css';
</style>