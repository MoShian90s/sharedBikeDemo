<template>
<el-card class='box-card' shadow='always'>
    <el-form size="medium" style="transition:1s" :disabled="availability">
        <el-form-item>
            <el-input placeholder="Unique ID" v-model="Customer_id" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item>
            <el-input placeholder="First Name" v-model="Customer_first_name"></el-input>
        </el-form-item>
        <el-form-item>
            <el-input placeholder="Last Name" v-model="Customer_last_name"></el-input>
        </el-form-item>
        <el-form-item>
            <el-input placeholder="Age" v-model="Customer_age"></el-input>
        </el-form-item>
        <el-form-item>
            <el-select v-model="Customer_gender" placeholder="Gender" style="width:100%">
                <el-option label="🧑 male" value="male"></el-option>
                <el-option label="👧 female" value="female"></el-option>
                <el-option label="👽 secret" value="secret"></el-option>
            </el-select>
        </el-form-item>
        <el-form-item>
            <el-input placeholder="Phone" v-model="Customer_phone_num"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button class="submitBtn" type="primary" round @click.native="update">commit</el-button>
        </el-form-item>
    </el-form>
</el-card>
</template>

<script>
import axios from 'axios';
import qs from 'qs';

export default {
    props:{
        newInfoMsg:Object,
    },
    watch:{
        newInfoMsg:function(){
            // console.log(this.newInfoMsg);
            this.Customer_id=this.newInfoMsg.Customer_id;
            this.Customer_first_name=this.newInfoMsg.Customer_first_name;
            this.Customer_last_name=this.newInfoMsg.Customer_last_name;
            this.Customer_age=this.newInfoMsg.Customer_age;
            this.Customer_gender=this.newInfoMsg.Customer_gender;
            this.Customer_phone_num=this.newInfoMsg.Customer_phone_num;
        }
    },
    data(){
        return{
            Customer_id:'',
            Customer_first_name:'',
            Customer_last_name:'',
            Customer_age:'',
            Customer_gender:'',
            Customer_phone_num:'',
        }
    },
    computed:{
        availability:function(){
            if(this.Customer_id!=''&this.Customer_first_name!=''&this.Customer_last_name!=''&this.Customer_age!=''){
                return false;
            }else{
                return true;
            }
        }
    },
    methods:{
        update(){
            let that=this;
            let payload=qs.stringify({
                customer_id:that.Customer_id,
                customer_first_name:that.Customer_first_name,
                customer_last_name:that.Customer_last_name,
                customer_age:that.Customer_age,
                customer_gender:that.Customer_gender,
                customer_phone_num:that.Customer_phone_num})
            axios.post(that.$baseURL+"/manager/editcustomerinfo/",payload)
                .then(function(response) {
                    if(response.status === 200){
                        that.$emit("update","update");
                        that.$notify.success({
                            title:'Update Operation',
                            message:'you have deleted ' + that.Customer_id
                        })
                    }
                })
                .catch(function () {
                    that.$notify.error({
                        title:'Update Operation',
                        message:'illegal operation'
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