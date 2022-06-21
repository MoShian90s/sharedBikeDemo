<template>
    <div>
        <visual-cards></visual-cards>

        <el-divider class="divider"><i class="el-icon-sort"></i></el-divider>

        <el-row :gutter="50" type="flex" justify="center" style="flex-wrap:wrap">
            <el-col :xs='24' :sm='24' :md='16' :lg='16' :xl='16'>
                <customer-table :notifyUpdate="notifyUpdate" v-on:select="selectUpdate"></customer-table>
            </el-col>
            <el-col :xs='24' :sm='24' :md='8' :lg='8' :xl='8'>
                <table-toolbar v-on:update="update" :newInfoMsg="Msg"></table-toolbar>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import CustomerTable from './Table'
import TableToolbar from './TableToolbar'
import VisualCards from './Visualization'

export default {
    data(){
        return{
            notifyUpdate:1,
            Msg:null,
        }
    },
    components: { 
        CustomerTable,
        TableToolbar,
        VisualCards,
    },
    methods:{
        update(){
            this.notifyUpdate=-(this.notifyUpdate);
        },
        selectUpdate(msg){
            this.Msg=msg;
        }
    }
}
</script>

<style scoped>
.InfoCards{
    margin-bottom: 10vh!important;
}
.divider{
    margin: 7vh 0 7vh 0;
}
</style>