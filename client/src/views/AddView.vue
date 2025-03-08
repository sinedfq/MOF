<script setup>
import StatusRow from '@/components/StatusRow.vue';
import SubCategoryRow from '@/components/SubCategoryRow.vue';
import TypeRow from '@/components/TypeRow.vue';
import CategoryRow from '@/components/CategoryRow.vue';
import AddTransRow from '@/components/AddTransRow.vue';



</script>

<template>
    <div class = "container">
        <AddTransRow style="margin-left: 10%;"/>
    </div>
    
    <div class = "container">
        <StatusRow style="margin-left: 10%;"/>
    </div>

    <div class = "container">
        <TypeRow style="margin-left: 10%;"/>
    </div>

    <div class = "container">
        <CategoryRow style="margin-left: 10%;"/>
    </div>

    <div class = "container">
        <SubCategoryRow style="margin-left: 10%;"/>
    </div>

</template>

<style>

.container {
    box-shadow: 0px 4px 8px 0px rgba(0,0,0,0.2);
    border-radius: 20px;
    align-content: center;
    width: 500px;
    height: 300px;
    margin-left: 30%;

}

</style>