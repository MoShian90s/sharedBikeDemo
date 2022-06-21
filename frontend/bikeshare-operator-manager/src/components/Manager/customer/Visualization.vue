<template>
    <el-row :gutter="50" type="flex" justify="center" style="flex-wrap:wrap">
        <el-col :xs='24' :sm='24' :md='8' :lg='8' :xl='8' class="visualCards">
            <el-card class='box-card' shadow='always'>
                <div ref="gender" style="height:40vh;"></div>
            </el-card>
        </el-col>
        <el-col :xs='24' :sm='24' :md='8' :lg='8' :xl='8' class="visualCards">
            <el-card class='box-card' shadow='always'>
                <div ref="age" style="height:40vh;"></div>
            </el-card>
        </el-col>
        <el-col :xs='24' :sm='24' :md='8' :lg='8' :xl='8' class="visualCards">
            <el-card class='box-card' shadow='always'>
                <div ref="serviceTime" style="height:40vh"></div>
            </el-card>
        </el-col>
    </el-row>
</template>

<script>
import axios from 'axios'

export default {
    data(){
        return{
            genderXaxis:[],
            genderYaxis:[]
        }
    },
    methods:{
        EchartsGender(){
            let that=this;
            axios.get(that.$baseURL+'/manager/customer_gender/')
                .then((response)=>{
                    let x=[];
                    let y=[];
                    response.data.forEach(element => {
                        x.push(element['Customer_gender'])
                        y.push(element['Count'])
                    });
                    var GenderChart=that.$echarts.init(that.$refs.gender);
                    var option={
                        tooltip: {
                            trigger: 'item'
                        },
                        title:{
                            text:"Gender"
                        },
                        legend:{
                            top: '5%',
                            left: 'center',
                        },
                        xAxis:{
                            data: x
                        },
                        yAxis:{},
                        series:[{
                            name:'Gender',
                            type: 'bar',
                            data: y
                        }]
                    };
                    // console.log("echarts:: gender visualization");
                    GenderChart.setOption(option);
                })
                .catch(function (error) {
                    console.log(error);
            });
        },
        EchartsAge(){
            let that=this;
            axios.get(that.$baseURL+'/manager/customer_age/')
                .then(function(response) {

                    let data=[];
                    response.data.forEach(element => {
                        let item={}
                        item['name']=element['name']
                        item['value']=element['value']
                        data.push(item)
                    });
                    
                    var AgeChart=that.$echarts.init(that.$refs.age);
                    var option={
                        title:{
                            text:"Age"
                        },
                        tooltip: {
                            trigger: 'item',
                        },
                        legend: {
                            bottom: '5%',
                            left: 'center',
                        },
                        series:[{
                            name: 'Age',
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
                    AgeChart.setOption(option);
                })
                .catch(function (error) {
                    console.log(error);
                });
            
        },
        EchartsUser(){
            let that=this;
            axios.get(that.$baseURL+'/manager/customer_order_history/')
                .then((response)=>{
                    let data=[]
                    response.data.forEach(element => {
                        let item={}
                        item['name']=element[1]
                        item['value']=element[2]
                        data.push(item)
                    });
                    var Chart=that.$echarts.init(that.$refs.serviceTime);
                    var option={
                        title:{
                            text:"Service Time"
                        },
                        tooltip: {
                            trigger: 'item',
                        },
                        legend: {
                            bottom: '5%',
                            left: 'center',
                        },
                        series:[{
                            name: 'time',
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
                    Chart.setOption(option);
                })
                .catch(function (error) {
                    console.log(error);
            });
        }
    },
    mounted(){
        this.EchartsGender();
        this.EchartsAge();
        this.EchartsUser();
    }
}
</script>