<template>
    <div>
        <el-row type="flex" :gutter="50" class="headDatasHeader">
            <el-col :xs='24' :sm='7' :md='7' :lg='6' :xl='6'>
                <el-card @click.native="switchToHolistic" class='box-card choiceCard' shadow='hover' body-style="height:100%;width:100%;display:flex;justify-content:space-evenly;align-items:center">
                    <span class="emojiTitle">🎞</span><span class="textTitle">Quick Look</span>
                </el-card>
            </el-col>

            <el-col :xs='24' :sm='7' :md='7' :lg='6' :xl='6' >
                <el-card @click.native="switchToTimeDefined" class='box-card choiceCard' shadow='hover' body-style="height:100%;width:100%;display:flex;justify-content:space-evenly;align-items:center">
                    <span class="emojiTitle">👁</span><span class="textTitle">Advanced Research</span>
                </el-card>
            </el-col>
            <transition mode="out-in" enter-active-class="slide-in-top" leave-active-class="slide-out-top" :duration="{ enter: 300, leave: 300 }">
            <el-col :xs='24' :sm='7' :md='7' :lg='6' :xl='6' v-if="mapConfig">
                <el-card @click.native="mapConfigDrawer=true" class='box-card choiceCard' shadow='hover' body-style="height:100%;width:100%;display:flex;justify-content:space-evenly;align-items:center;background:#e8e8e8">
                    <span class="emojiTitle">🛠</span><span class="textTitle">MapConfig</span>
                </el-card>
            </el-col>
            </transition>
        </el-row>
        <el-drawer
            title="map visualization configuration"
            :visible.sync="mapConfigDrawer"
            :direction="'btt'"
            :modal="false"
            size="65%" style="overflow:auto">
            <bike-map-config></bike-map-config>
        </el-drawer>

        <transition mode="out-in" enter-active-class="slide-in-left" leave-active-class="slide-out-left" :duration="{ enter: 300, leave: 300 }">
            <component 
                :is="headDatas" 
                ></component>
        </transition>
    </div>
</template>

<script>
import Holistic from './Holistic/Holistic'
import BikeMapConfig from './Holistic/BikeMapConfig'
import TimeDefined from './TimeDefined/TimeDefined'

export default {
    components:{
        Holistic,
        BikeMapConfig,
        TimeDefined
    },
    data(){
        return{
            headDatas:'Holistic',
            mapConfig: true,
            mapConfigDrawer: false,
        }
    },
    computed:{
        VisualCardsVisible:function(){
            if(this.headDatas==='TimeDefined'){
                return false
            }else{
                return true
            }
        }
    },
    methods:{
        switchToHolistic(){
            this.headDatas='Holistic'
            this.mapConfig=true;
        },
        switchToTimeDefined(){
            this.headDatas='TimeDefined'
            this.mapConfig=false;
        }
    }
}


</script>

<style scoped>
.divider{
    margin: 7vh 0 7vh 0;
}
.choiceCard{
    height: 15vh;
    cursor: pointer;
    /* transition: 0.3s; */
}
.headDatasHeader{
    margin-bottom: 5vh;
}
.emojiTitle{
    font-size:3rem;
}
.textTitle{
    font-size:1.5rem;
}
.slide-in-left {
	-webkit-animation: slide-in-left 0.3s cubic-bezier(0.250, 0.460, 0.450, 0.940) both;
	animation: slide-in-left 0.3s cubic-bezier(0.250, 0.460, 0.450, 0.940) both;
}
@-webkit-keyframes slide-in-left {
  0% {
    -webkit-transform: translateX(-1000px);
            transform: translateX(-1000px);
    opacity: 0;
  }
  100% {
    -webkit-transform: translateX(0);
            transform: translateX(0);
    opacity: 1;
  }
}
@keyframes slide-in-left {
  0% {
    -webkit-transform: translateX(-1000px);
            transform: translateX(-1000px);
    opacity: 0;
  }
  100% {
    -webkit-transform: translateX(0);
            transform: translateX(0);
    opacity: 1;
  }
}
.slide-out-left {
	-webkit-animation: slide-out-left 0.3s cubic-bezier(0.550, 0.085, 0.680, 0.530) both;
	animation: slide-out-left 0.3s cubic-bezier(0.550, 0.085, 0.680, 0.530) both;
}
@-webkit-keyframes slide-out-left {
  0% {
    -webkit-transform: translateX(0);
            transform: translateX(0);
    opacity: 1;
  }
  100% {
    -webkit-transform: translateX(-1000px);
            transform: translateX(-1000px);
    opacity: 0;
  }
}
@keyframes slide-out-left {
  0% {
    -webkit-transform: translateX(0);
            transform: translateX(0);
    opacity: 1;
  }
  100% {
    -webkit-transform: translateX(-1000px);
            transform: translateX(-1000px);
    opacity: 0;
  }
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
</style>