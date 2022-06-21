<template>
	<el-container>
		<el-main class="loginBackground" :class="color">
			<!-- vue transition setting for componenets -->
			<transition mode="out-in" enter-active-class="slide-in-top" leave-active-class="slide-out-top" :duration="{ enter: 300, leave: 300 }">
				<component :is="frame" v-on:ToLoginForm="switchFrame" :type="type" :target="target"></component>
			</transition>
		</el-main>
	</el-container>
</template>

<script>
import LoginChoice from './components/LoginChoice.vue'
import LoginForm from './components/LoginForm.vue'


export default {
	components:{
		LoginChoice,
		LoginForm,
	},
	data(){
		return{
			type:'',
			frame:'LoginChoice',
			loginInfo:{
				username:'',
				pass:'',
			},
			color:'aqua',
		}
	},
	methods:{
		switchFrame(e){
			if(e==='Choice'){
				this.frame='LoginChoice';
			}else if(e==='Operator'|e==='Manager'){
				this.frame='LoginForm';
			}
			this.type=e;
		},
	}
}
</script>

<style scoped>
	.loginBackground{
		display: flex;
		align-items: center;
		justify-content:center;
		width: 100vw;
		height: 100vh;
		transition: 0.3s;
		background-color: aqua;
	}

	.loginForm{
		padding:0;
		margin:0;
	}

	/* all code blocks below are animation class css */
	.slide-in-top {
	-webkit-animation: slide-in-top 0.3s cubic-bezier(0.250, 0.460, 0.450, 0.940) both;
			animation: slide-in-top 0.3s cubic-bezier(0.250, 0.460, 0.450, 0.940) both;
	}

	/**
	* ----------------------------------------
	* animation slide-in-top
	* ----------------------------------------
	*/
	@-webkit-keyframes slide-in-top {
	0% {
		-webkit-transform: translateY(-1000px);
				transform: translateY(-1000px);
		opacity: 0;
	}
	100% {
		-webkit-transform: translateY(0);
				transform: translateY(0);
		opacity: 1;
	}
	}
	@keyframes slide-in-top {
	0% {
		-webkit-transform: translateY(-1000px);
				transform: translateY(-1000px);
		opacity: 0;
	}
	100% {
		-webkit-transform: translateY(0);
				transform: translateY(0);
		opacity: 1;
	}
	}

	.slide-out-top {
		-webkit-animation: slide-out-top 0.3s cubic-bezier(0.550, 0.085, 0.680, 0.530) both;
				animation: slide-out-top 0.3s cubic-bezier(0.550, 0.085, 0.680, 0.530) both;
	}

	/**
	* ----------------------------------------
	* animation slide-out-top
	* ----------------------------------------
	*/
	@-webkit-keyframes slide-out-top {
	0% {
		-webkit-transform: translateY(0);
				transform: translateY(0);
		opacity: 1;
	}
	100% {
		-webkit-transform: translateY(-1000px);
				transform: translateY(-1000px);
		opacity: 0;
	}
	}
	@keyframes slide-out-top {
	0% {
		-webkit-transform: translateY(0);
				transform: translateY(0);
		opacity: 1;
	}
	100% {
		-webkit-transform: translateY(-1000px);
				transform: translateY(-1000px);
		opacity: 0;
	}
	}
	/* scrollbar css configuration, waitting for update */
	::-webkit-scrollbar{
		position:fixed;
		z-index: 3;
		right:0;
		width: 25px;
		background-color: transparent;
	}

</style>
