<template>
<el-card class='box-card' shadow='always'>
    <el-form size="medium" :inline="true">
        <el-form-item>
            <el-input placeholder="Input Key Word to Delete" v-model="DelKey"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button @click.native="DelInfo">Delete</el-button>
        </el-form-item>
    </el-form>
</el-card>
</template>

<script>
import axios from 'axios';
import qs from 'qs'

export default {
    data(){
        return{
            DelKey:'',
        }
    },
    methods:{
        DelInfo(){
            let that=this;
            let payload=qs.stringify({customer_id:that.DelKey});
            axios.post(that.$baseURL+"/manager/deletecustomerinfo/",payload)
                .then(function() {
                    // console.log(response.data);
                    that.$emit("update","update");
                    that.$notify.success({
                        title:'Delete Operation',
                        message:'you have deleted ' + that.DelKey
                    });
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