<template>
<el-card  class='box-card' shadow='always' body-style="display:flex;justify-content:center;align-items:center;padding:5% 7% 5% 7%">
    <el-form size="medium" style="transition:1s;width:100%">
        <el-form-item>
            <el-input placeholder="Name" v-model="Username"></el-input>
        </el-form-item>
        <el-form-item>
            <el-input placeholder="Password" v-model="password"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button class="submitBtn" round @click.native="create">commit</el-button>
        </el-form-item>
    </el-form>
</el-card>
</template>

<script>
import axios from 'axios';
import qs from 'qs';
import { sharedStore } from '../Table';

export default {
    data(){
        return{
            Username:'',
            password:'',
            user_type:'Operator',
        }
    },
    methods:{
        create(){
            let that=this;
            let payload=qs.stringify({username:that.Username,password:that.password,user_type:that.user_type})
            axios.post(that.$baseURL+"/manager/addoperatorinfo/",payload)
                .then(function(response) {
                    if(response.status === 200){
                        that.$notify.success({  
                            title:'Create Operation',
                            message:'you have Create ' + that.operator_id
                        })
                        sharedStore.refresher(that.$baseURL);
                    }
                })
                .catch(function () {
                    that.$notify.error({
                        title:'Create Operation',
                        message:'the same id existing'
                    });
            });
        }
    }
}
</script>

<style scoped>
.submitBtn{
    width:100%;margin-top:3vh;
}
.submitBtn:hover{
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
}
</style>