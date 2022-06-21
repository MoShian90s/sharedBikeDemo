<template>
<div>
    <div class="header">
        <span class="icon moreData" @click="drawerL=true">🐎</span>
        <span class="moreData el-icon-more" @click="drawerR=true"></span>
    </div>

    <el-drawer ref="drawer" title="QUICK START" :visible.sync="drawerR" direction="rtl" :size="'100%'" close-on-press-escape>
        
        <el-container style="height:100%;">
            <el-main style="height:100%;display:flex;align-items:center;margin:0 10vw 0 10vw;justify-content:center;">
                <el-row type="flex" justify="space-around" style="width:100%;flex-wrap:wrap;">
                    <el-col class="databaseChoice" :xs='18' :sm='18' :md='8' :lg='8' :xl='8'>
                        <el-card class='box-card choiceCard' shadow='hover' header="CUSTOMER" @click.native="SwitchToCustomer">
                            <span class="emojiSize">🙎‍♂️</span>
                        </el-card>
                    </el-col>
                    <el-col class="databaseChoice" :xs='18' :sm='18' :md='8' :lg='8' :xl='8'>
                        <el-card class='box-card choiceCard' shadow='hover' header="OPERATOR" @click.native="SwitchToOperator">
                            <span class="emojiSize">👩‍🔧</span>
                        </el-card>
                    </el-col>
                    <el-col class="databaseChoice" :xs='18' :sm='18' :md='8' :lg='8' :xl='8'>
                        <el-card class='box-card choiceCard' shadow='hover' header="BIKE" @click.native="SwitchToBike">
                            <span class="emojiSize">👩‍💼</span>
                        </el-card>
                    </el-col>
                </el-row>
            </el-main>
        </el-container>

    </el-drawer>

    <el-drawer :show-close="false" ref="Profiledrawer" :visible.sync="drawerL" direction="ltr" :size="'25%'" close-on-press-escape>
        
        <el-row type="flex" justify="space-around" style="margin:5vh 10% 5vh 10%;flex-wrap:wrap;">
            <el-col :xs='24' :sm='24' :md='24' :lg='24' :xl='24' class="ProfileCard">
                
                    <el-row type="flex" justify="space-around" style="flex-wrap:wrap;">
                        <el-col :xs='24' :sm='24' :md='24' :lg='24' :xl='24'>
                            <el-avatar :size="100" :src="'http://ww1.sinaimg.cn/large/006hPLGily1gnlf9281rmj30po0pjjs0.jpg'" fit="scale-down" style="box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)"></el-avatar>
                        </el-col>
                        <el-col :xs='24' :sm='24' :md='24' :lg='24' :xl='24'>
                            <h1>YIFAN YUAN</h1>
                        </el-col>
                        <el-col :xs='24' :sm='24' :md='24' :lg='24' :xl='24'>
                            <el-tag type="success">online</el-tag>
                        </el-col>
                    </el-row>
                
            </el-col>
            <el-col :xs='24' :sm='24' :md='24' :lg='24' :xl='24'>
                <el-divider></el-divider>
            </el-col>
            <el-col :xs='24' :sm='24' :md='24' :lg='24' :xl='24'>
                <el-link class="ProfileMenu" icon="el-icon-warning-outline" :underline="false" @click.native="logOut">Log Out</el-link>
            </el-col>
        </el-row>

    </el-drawer>
</div>
</template>

<script>
import axios from 'axios';
import qs from 'qs';
axios.defaults.withCredentials=true;

export default {
    data(){
        return{
            drawerR:false,
            drawerL:false,
        }
    },
    methods:{
        SwitchToCustomer(){
            this.$emit("SwitchToDatas",'Customer');
            this.$refs.drawer.closeDrawer();
        },
        SwitchToOperator(){
            this.$emit("SwitchToDatas",'Operator');
            this.$refs.drawer.closeDrawer();
        },
        SwitchToBike(){
            this.$emit("SwitchToDatas",'Bike');
            this.$refs.drawer.closeDrawer();
        },
        logOut(){
            let that=this;
            let payload=qs.stringify({username:that.$session.get('username'),type:that.$session.get('type')})
            axios.post(that.$baseURL+'/signout/',payload)
                .then(function() {
                    that.$session.destroy()
                    that.$router.push('/')
                    that.$notify.success({
                        title: 'log out',
                        message: 'you have successfully logged out',
                    });
                })
                .catch(function (error) {
                    if(error.response.status===404){
                        that.$notify.error({
                            title: 'log out',
                            message: 'user not found',
                        });
                    }
            });
        }
    }
}
</script>

<style scoped>
.header{
    width:100%;
    height:10vh;
    min-height: 30px;
    background-color: #5470c6;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 4px 5px rgba(0, 0, 0, .2)
}
.databaseChoice{
    padding:0vh 2.5vw 5vh 2.5vw;
}
.choiceCard{
    cursor:pointer;

}
.ProfileCard{
    margin-bottom: 5vh;
    cursor:pointer;
    font-size:1.2em;
}
.ProfileMenu{
    width:100%;
    padding: 2.5vh 0 2.5vh 0;
    font-size:1.2em;
    transition: 0.3s;
}
.ProfileMenu:hover{
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
}
@media only screen and (min-width:992px) {
    .emojiSize{
        font-size: 7rem;
    }
    .moreData{
        padding:1vh 1vw 1vh 1vw;
        margin-right: 1.5vw;
        margin-left: 1.5vw;
        font-size: 200%;
        cursor:pointer;
        transition: 0.3s;
    }
    .moreData:hover{
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.2);
    }
}
@media only screen and (max-width:992px) {
    .emojiSize{
        font-size: 2rem;
    }
    .moreData{
        padding:1vh 1vw 1vh 1vw;
        margin-right: 5vw;
        margin-left: 5vw;
        font-size: 200%;
        cursor:pointer;
        transition: 0.3s;
    }
    .moreData:hover{
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.2);
    }
}
</style>