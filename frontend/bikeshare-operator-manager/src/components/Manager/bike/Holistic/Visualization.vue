<template>
<div>
    <el-row :gutter="50" type="flex" justify="center" style="flex-wrap:wrap">
        <el-col :xs='24' :sm='24' :md='16' :lg='16' :xl='16'>
            <el-card class='box-card' shadow='always'>
                <div ref="brand" style="height:40vh;"></div>
            </el-card>
        </el-col>
        <el-col :xs='24' :sm='24' :md='8' :lg='8' :xl='8'>
            <el-card class='box-card' shadow='always'>
                <div ref="status" style="height:40vh"></div>
            </el-card>
        </el-col>
    </el-row>
</div>
</template>

<script>
import axios from 'axios'


export default {
    
    methods:{
        EchartsBrand(){
            let that=this;
            axios.get(that.$baseURL+'/manager/bike_brand/')
                .then(function(response) {
                    let x=[];
                    let y=[];
                    response.data.forEach(element => {
                        x.push(element['Brand'])
                        y.push(element['Count'])    
                    });
                    var BrandChart=that.$echarts.init(that.$refs.brand);
                    var option={
                        tooltip: {
                            trigger: 'item'
                        },
                        title:{
                            text:"Brand"
                        },
                        legend:{
                            top: '5%',
                            left: 'center',
                        },
                        xAxis:{
                            data:x
                        },
                        yAxis:{},
                        series:[{
                            name:'Brand',
                            type: 'bar',
                            data:y,
                        }]
                    };
                    BrandChart.setOption(option);
                })
                .catch(function (error) {
                    console.log(error);
                });
        },
        EchartsStatus(){
            let that=this;
            axios.get(that.$baseURL+'/manager/bike_status/')
                .then(function(response) {
                    let data=[]

                    response.data.forEach(element => {
                        let item={}
                        item['value']=element['value']
                        item['name']=element['Status']
                        data.push(item)  
                    });
                    that.data=data;
                    var StatusChart=that.$echarts.init(that.$refs.status);
                    var option={
                        title:{
                            text:"Status"
                        },
                        tooltip: {
                            trigger: 'item',
                        },
                        legend: {
                            bottom: '5%',
                            left: 'center',
                        },
                        series:[{
                            name: 'Status',
                            type: 'pie',
                            radius:['40%','70%'],
                            avoidLabelOverlap:false,
                            itemStyle:{
                                borderRadius:10,
                                borderColor:'#fff',
                                borderWidth:2
                            },
                            label:{
                                show:false,
                                position:'center',
                            },
                            emphasis:{
                                label:{
                                    show:true,
                                    fontSize:'40',
                                    fontWeight:'bold'
                                }
                            },
                            labelLine:{
                                show:false
                            },
                            data:data
                        }],
                    };
                    StatusChart.setOption(option);
                })
                .catch(function (error) {
                    console.log(error);
                });     
        },
        
    },
    mounted(){
        this.EchartsBrand();
        this.EchartsStatus();

    }
}
</script>

<style scoped>
.visualCards{
    margin: 5vh 0 0 0;
}
</style>