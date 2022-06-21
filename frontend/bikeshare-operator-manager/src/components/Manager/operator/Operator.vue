<template>
    <div>
        <el-row :gutter="50" type="flex" justify="center" style="flex-wrap:wrap">
            <el-col :xs='24' :sm='24' :md='16' :lg='16' :xl='16'>
                <operator-table></operator-table>
            </el-col>
            <el-col :xs='24' :sm='24' :md='8' :lg='8' :xl='8'>
                <el-row type="flex" justify="center" style="flex-wrap:wrap">
                    <el-col class="InfoCards" :xs='24' :sm='24' :md='24' :lg='24' :xl='24'>
                        <table-toolbar></table-toolbar>
                    </el-col>
                </el-row>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import OperatorTable from './Table'
import TableToolbar from './TableToolbar'

export default {
    components: { 
        OperatorTable,
        TableToolbar,
    },
    data(){
        return{
            operators:[
                {name:"yifan yuan", status:"online"},
                {name:"kiki lee", status:"online"},
                {name:"dudu lee", status:"offline"},
            ]
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