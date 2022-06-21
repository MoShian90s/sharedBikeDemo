<template>
<el-card class="loginFrame" body-style="padding:5% 10% 10% 10% ;margin:0;width:100%;height:100%;display:flex;align-item:center;">
    <el-row type="flex" style="flex-wrap:wrap;align-items:center;justify-content:center;width:100%">
        <el-col style="text-align:right" :xs='24' :sm='24' :md='24' :lg='24' :xl='24'>
            <span class="backBtn" @click="backTochoice">🐎 TO LOGIN PAGE</span>
        </el-col>
        <el-col class="loginForm" :xs='24' :sm='24' :md='24' :lg='24' :xl='24'><h1>Hi, {{this.type}}</h1></el-col>
        <el-col class="loginForm" :xs='24' :sm='24' :md='24' :lg='24' :xl='24'>
            <el-form :model="loginInfo" :rules="rules" status-icon ref="loginInfo">
                <el-form-item prop="username">
                    <el-input v-model="loginInfo.username" placeholder="username/mail"></el-input>
                </el-form-item>
                <el-form-item prop="pass">
                    <el-input v-model="loginInfo.pass" placeholder="password" type="password" autocomplete="off" ></el-input>
                </el-form-item>

                <el-form-item>
                    <el-button class="loginbtn" type="primary" @click="submitForm('loginInfo')">Log in</el-button>
                </el-form-item>
            </el-form>
        </el-col>
    </el-row>
</el-card>
</template>

<script>
import axios from 'axios';
import qs from 'qs';
axios.defaults.withCredentials=true;

export default {
	data(){
        var validateName=(rule,value,callback)=>{
            if(value===''){
                callback(new Error("username is null"));
            }else{
                var re=/([a-zA-Z0-9]+)@([a-zA-Z0-9]+)(\.)([a-zA-Z0-9]+)/;
                if(re.test(value)){
                    callback();//if use mailbox, we should distinguish them as different data format in database search.
                }
                callback();
            }
        };
        var validatePass=(rule,value,callback)=>{
            if(value===''){
                callback(new Error("password is null"));
            }else{
                callback();
            }
        };

		return{
			loginInfo:{
				username:'',
				pass:'',
            },
            // element UI form attributes, for validation
            rules:{
                username:[
                    {validator:validateName, trigger:'blur'}
                ],
                pass:[
                    {validator:validatePass, trigger:'blur'}
                ],
            }
		}
    },
    methods:{
        // waiting for writing specific logic
        // the submit function needs the axios post here
        submitForm(formName){
            let that=this;
            that.$refs[formName].validate((valid) => {
                if (valid) {
                    console.log('Login:: information submitted');
                    let payload=qs.stringify({username:that.loginInfo.username,password:that.loginInfo.pass,user_type:that.type})
                    axios.post(that.$baseURL+'/signin/',payload)
                        .then(function(response) {
                            if(response.status === 200){
                                that.$session.start()
                                that.$session.renew(response.data)
                                that.$session.set('type',that.type)
                                that.$session.set('username',that.loginInfo.username)
                                if(that.type==="Operator"){
                                  that.$session.set("Operator_id",response.data.id)
                                  that.$router.push("/operator")
                                }else{
                                  that.$router.push("/manager");
                                }
                                that.$notify.success({
                                    title:that.loginInfo.username,
                                    message:'you have successfully logged in'
                                })
                            }
                        })
                        .catch(function (error) {
                            if(error.response.status === 401){
                                that.$notify.error({
                                    title:'Log in Failed',
                                    message:'password incorrect'
                                })
                            }else if(error.response.status === 404){
                                that.$notify.error({
                                    title:'Log in Failed',
                                    message:'username incorrect'
                                })
                            }
                    });
                } else {
                    console.log('Login:: error submit');
                    return false;
                }
            });
        },
        backTochoice(){
            this.$emit("ToLoginForm",'Choice');
        }
    },
    props:{
        type:String,
    }
}
</script>

<style scoped>
    .loginbtn{
		width:100%;
	}
    .loginbtn:hover{
		box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
	}
    .loginForm{
		padding:0;
		margin:0;
    text-align: center;
	}
    .backBtn{
        background-color: aqua;
        cursor:pointer;
    }

	@media only screen and (min-width:500px) {
		.loginFrame{
			height:60vh;
			width: 50vh;
			box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
			display:flex;
			align-items: center;
			justify-content: center;
		}

	}

	@media only screen and (max-width:500px) {
		.loginFrame{
			height:60vh;
			width: 90vw;
			box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
			display:flex;
			align-items: center;
			justify-content: center;
		}
	}
</style>
