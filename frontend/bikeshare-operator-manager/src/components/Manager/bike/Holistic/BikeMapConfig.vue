<template>
<div style="overflow:scroll;height:100%">
    <h1>HeatMap</h1>
    <el-row type="flex" style="margin:0 20vw 0 20vw;flex-wrap:wrap">
        <el-col class="ConfigCol" :xs='3' :sm='3' :md='3' :lg='3' :xl='3' style="display:flex;align-items:center;">
            <span>Visibility</span>
        </el-col>
        <el-col class="ConfigCol" :xs='20' :sm='20' :md='20' :lg='20' :xl='20' style="display:flex;justify-content:flex-start">
            <el-switch
                v-model="HeatMapVisbility"
                active-color="#5470c6"
                inactive-color="#ff4949"
                >
            </el-switch>
        </el-col>

        <el-col class="ConfigCol" :xs='3' :sm='3' :md='3' :lg='3' :xl='3' style="display:flex;align-items:center">
            <span>Radius</span>
        </el-col>
        <el-col class="ConfigCol" :xs='20' :sm='20' :md='20' :lg='20' :xl='20'>
            <el-slider
                v-model="HeatMapRadius"
                :step="10"
                show-stops
                >
            </el-slider>
        </el-col>
    </el-row>
    <h1>Marker</h1>
    <el-row type="flex" style="margin:0 20vw 0 20vw;flex-wrap:wrap">
        <el-col class="ConfigCol" :xs='3' :sm='3' :md='3' :lg='3' :xl='3' style="display:flex;align-items:center;">
            <span>Bike Visibility</span>
        </el-col>
        <el-col class="ConfigCol" :xs='20' :sm='20' :md='20' :lg='20' :xl='20' style="display:flex;justify-content:flex-start">
            <el-switch
                v-model="BikeMarkerVisbility"
                active-color="#5470c6"
                inactive-color="#ff4949"
               >
            </el-switch>
        </el-col>
        <el-col class="ConfigCol" :xs='3' :sm='3' :md='3' :lg='3' :xl='3' style="display:flex;align-items:center;">
            <span>Self Visibility</span>
        </el-col>
        <el-col class="ConfigCol" :xs='20' :sm='20' :md='20' :lg='20' :xl='20' style="display:flex;justify-content:flex-start">
            <el-switch
                v-model="SelfMarkerVisbility"
                active-color="#5470c6"
                inactive-color="#ff4949"
                >
            </el-switch>
        </el-col>
    </el-row>
    
</div>
</template>

<script>
import Vue from 'vue'
export default {
    computed:{
        HeatMapVisbility:{
            get(){
                return sharedConfig.HeatMapVisbility
            },
            set(value){
                sharedConfig.HeatMapVisbility=value
            }
        },
        HeatMapRadius:{
            get(){
                return sharedConfig.HeatMapRadius
            },
            set(value){
                sharedConfig.HeatMapRadius=value
            }
        },
        BikeMarkerVisbility:{
            get(){
                return sharedConfig.BikeMarkerVisbility
            },
            set(value){
                sharedConfig.BikeMarkerVisbility=value
            }
        },
        SelfMarkerVisbility:{
            get(){
                return sharedConfig.SelfMarkerVisbility
            },
            set(value){
                sharedConfig.SelfMarkerVisbility=value
            }
        },
    },
    methods:{
        // HeatMapVisibChange(value){
        //     sharedConfig.HeatMapVisbility=value
        // },
        // HeatMapRadiusChange(value){
        //     sharedConfig.HeatMapRadius=value
        // },
        // BikeMarkerVisbilityChange(){
        //     sharedConfig.BikeMarkerVisbility=60
        // },
        // SelfMarkerVisbilityChange(value){
        //     sharedConfig.SelfMarkerVisbility=value
        // }
    }

}

export var sharedConfig=Vue.observable({HeatMapVisbility:false,HeatMapRadius:40,BikeMarkerVisbility:false,SelfMarkerVisbility:false})
</script>

<style scoped>
.ConfigCol{
    margin:0 0 5% 0;
}
</style>