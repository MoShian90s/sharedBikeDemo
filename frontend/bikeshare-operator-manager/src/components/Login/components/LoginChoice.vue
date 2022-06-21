<template>

    <el-card class="loginFrame"  body-style="padding:10% 10% 10% 10% ;margin:0;width:100%;height:100%;display:flex;align-item:center;">
        <el-row type="flex" style="flex-wrap:wrap;align-items:center;justify-content:center;width:100%">
            <el-col class="loginChoice" :xs='24' :sm='24' :md='24' :lg='24' :xl='24'><span class="title">🐎..........</span></el-col>
            <el-col class="loginChoice" :xs='24' :sm='24' :md='24' :lg='24' :xl='24'>
                <el-row type="flex" style="flex-wrap:wrap;align-items:center;justify-content:center;width:100%">
                    <el-col class="loginChoice" :xs='24' :sm='24' :md='24' :lg='24' :xl='24'>
                        <el-button round class="choicebtn" @click.native="switchToOperator">👨‍🏭 Login as Operator</el-button></el-col>
                    <el-col class="loginChoice" :xs='24' :sm='24' :md='24' :lg='24' :xl='24'>
                        <el-button round class="choicebtn" @click.native="switchToManager">👩‍💻 Login as Manager</el-button></el-col>
                    <el-col class="loginChoice" :xs='24' :sm='24' :md='24' :lg='24' :xl='24'>
                        <el-button round class="choicebtn" @click.native="switchToCustomer">👩‍💻 Login as Customer</el-button></el-col>
                </el-row>
            </el-col>
        </el-row>
    </el-card>

</template>

<script>
export default {
    data(){
        return{
            isExit:'slide-in-left',
        }
    },
    methods:{
        switchToOperator(){
            this.$emit("ToLoginForm",'Operator');
        },
        switchToManager(){
            this.$emit("ToLoginForm",'Manager');
        },
        switchToCustomer(){
            window.location.href='customer/'
        }
    }
}
</script>

<style scoped>
    .title{
        font-size: 200%;
    }
    .loginChoice{
        padding:0;
        margin:0;
        text-align: center;
    }
    .choicebtn{
        width: 100%;
        margin: 0 0 10% 0!important;
    }
    .choicebtn:hover{
        width: 100%;
        margin: 0 0 10% 0!important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
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
