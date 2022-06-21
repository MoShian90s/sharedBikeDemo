<template>
<el-card class='box-card' shadow='always' body-style="display:flex;justify-content:center;align-items:center;padding:5% 7% 5% 7%">
    <el-form size="medium" :inline="true">
        <el-form-item>
            <el-input placeholder="Input Unique ID to Delete" v-model="operator_id"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button @click.native="Delete">commit</el-button>
        </el-form-item>
    </el-form>
</el-card>
</template>

<script>
import qs from 'qs'
import axios from 'axios'
import { sharedStore } from '../Table';
axios.defaults.withCredentials=true;

export default {
    data(){
        return{
            operator_id:'',
        }
    },
    methods:{
        Delete(){
            let that=this;
            let payload=qs.stringify({operator_id:that.operator_id})
            axios.post(that.$baseURL+"/manager/deleteoperatorinfo/",payload)
                .then(function(response) {
                    if(response.status === 200){
                        that.$notify.success({  
                            title:'Delete Operation',
                            message:'you have deleted ' + that.Customer_id
                        })
                        sharedStore.refresher(that.$baseURL);
                    }
                })
                .catch(function () {
                    that.$notify.error({
                        title:'Delete Operation',
                        message:'illegal operation'
                    });
            });
        }
    }
}
</script>

<style scoped>
.el-form{
    display: flex;
    justify-content: space-around;
}
.el-input{
    width:100%;
}
.el-button:hover{
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
}
</style>