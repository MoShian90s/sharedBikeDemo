<template>
<div style="width:100%">

    <bike-map></bike-map>

    <el-row :gutter="50" type="flex" style="flex-wrap:wrap;height:auto">
        <el-col :xs='24' :sm='24' :md='16' :lg='16' :xl='16'>
            <bike-table></bike-table>
        </el-col>
        <el-col :xs='24' :sm='24' :md='8' :lg='8' :xl='8'>
            <bike-toolbar></bike-toolbar>
        </el-col>
    </el-row>

    <el-divider class="divider"><i class="el-icon-sort"></i></el-divider>

    <visual-cards></visual-cards>

</div>
</template>

<script>
import BikeTable from './Table/Table'
import BikeToolbar from './Table/TableToolbar'
import VisualCards from './Visualization'
import BikeMap from './BikeMap'

export default {
    components:{
        BikeTable,
        BikeToolbar,
        VisualCards,
        BikeMap,
    }
}
</script>

<style scoped>
.divider{
    margin: 7vh 0 7vh 0;
}
</style>