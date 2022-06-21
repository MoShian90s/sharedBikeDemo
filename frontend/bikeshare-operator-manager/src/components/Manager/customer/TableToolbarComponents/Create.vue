<template>
<el-card class='box-card' shadow='always'>
    <el-form size="medium" style="transition:1s" :disabled="availability">
        <el-form-item>
            <el-input placeholder="Username" v-model="Customer_username"></el-input>
        </el-form-item>
        <el-form-item>
            <el-input placeholder="Password" v-model="Customer_password"></el-input>
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
            <el-input placeholder="Card Number" v-model="Customer_cardNumber"></el-input>
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
            <el-button class="submitBtn" type="primary" round @click.native="create">commit</el-button>
        </el-form-item>
    </el-form>
</el-card>
</template>

<script>
import axios from 'axios';
import qs from 'qs';

export default {
    data(){
        return{
            Customer_username:'',
            Customer_first_name:'',
            Customer_last_name:'',
            Customer_age:'',
            Customer_gender:'',
            Customer_phone_num:'',
            Customer_password:'',
            Customer_cardNumber:'',
        }
    },
    methods:{
        create(){
            let that=this;
            let payload=qs.stringify({
                username:that.Customer_username,
                password:that.Customer_password,
                first_name:that.Customer_first_name,
                last_name:that.Customer_last_name,
                age:that.Customer_age,
                gender:that.Customer_gender,
                phone_number:that.Customer_phone_num,
                cardNumber:that.Customer_cardNumber,})
            axios.post(that.$baseURL+"/manager/addcustomerinfo/",payload)
                .then(function(response) {
                    if(response.status === 200){
                        that.$emit("update","update");
                        that.$notify.success({  
                            title:'Create Operation',
                            message:'you have created ' + that.customer_first_name
                        })
                    }
                })
                .catch(function () {
                    that.$notify.error({
                        title:'Create Operation',
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