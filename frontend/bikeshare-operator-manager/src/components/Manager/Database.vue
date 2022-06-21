<template>
<div id="app">
	<mo-header v-on:SwitchToDatas="SwitchToDatas"></mo-header>
    <el-container>

	<el-main style="margin-left:6vw;margin-right:6vw;padding:10vh 1vw 10vh 1vw!important">
		<transition mode="out-in" enter-active-class="slide-in-top" leave-active-class="slide-out-top" :duration="{ enter: 300, leave: 300 }">
			<component :is="PannelSwitcher"></component>
		</transition>
    </el-main>

    </el-container>
</div>
</template>

<script>
import Bike from './bike/Bike'
import Customer from './customer/Customer'
import Operator from './operator/Operator'
import MoHeader from './header/HeadDrawer'

export default {
  name: 'app',
  components: {
	Operator,
	Bike,
    Customer,
	MoHeader
  },
  data(){
    return{
      toolbarObject:[],
      PannelSwitcher:'Customer',
    }
  },
  methods:{
    SwitchToDatas(data){
		this.PannelSwitcher=data;
	}
  },
  beforeCreate:function(){
	if (!this.$session.exists()) {
		this.$router.push('/')
		this.$notify.error({
			title:'no log information registered',
			message:'you need to log in first'
		})
	}
  }
}
</script>


<style scoped>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.el-header{
  padding: 0!important;;
}
.div-button{
  padding:0;margin:0;height:100%;width:100%;cursor:pointer;
}

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



</style>
