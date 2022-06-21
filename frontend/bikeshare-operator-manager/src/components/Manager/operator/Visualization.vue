<template>
<el-row :gutter="50" type="flex" style="flex-wrap:wrap">
    <el-col :xs='24' :sm='24' :md='24' :lg='24' :xl='24'>
        <el-card class='box-card' shadow='always' body-style="height:auto;">
            <div ref="status" style="height:40vh;"></div>
        </el-card>
    </el-col>
    <el-col :xs='24' :sm='24' :md='24' :lg='24' :xl='24' style="margin-top:5vh!important;">
        <el-card class='box-card' shadow='always' body-style="height:auto;">
            <div ref="complaints" style="height:40vh;"></div>
        </el-card>
    </el-col>
</el-row>
</template>

<script>
import axios from 'axios'

export default {

    data(){
        return{
            data:'',
        }
    },
    methods:{
        EchartsOperatorStatus(){
            let that=this;
            axios.get(that.$baseURL+'/manager/operator_login_status/')
                .then(function(response) {
                    let data=[]
                    response.data.forEach(element => {
                        let item={}
                        if(element['Login_status']===false){
                            item['name']="offline"
                        }else{
                            item['name']="online"
                        }
                        item['value']=element['Count']
                        data.push(item)   
                    });
                    that.data=data;
                    var Chart=that.$echarts.init(that.$refs.status);
                    var option={
                        tooltip: {
                            trigger: 'item',
                        },
                        legend: {
                            bottom: '5%',
                            left: 'center',
                        },
                        title:{
                            text:"Login Status"
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
                                position:'center'
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
                        }]
                    };

                    Chart.setOption(option);
                })
                .catch(function (error) {
                    console.log(error);
                });
            
        },
        EchartsComplaintsStatus(){
            let that=this;
            axios.get(that.$baseURL+'/manager/operator_complaint_status/')
                .then(function(response) {
                    let data=[]
                    response.data.forEach(element => {
                        let item={}
                        item['name']=element['Status']
                        item['value']=element['Count']
                        data.push(item)
                    });
                    that.data=data;
                    var Chart=that.$echarts.init(that.$refs.complaints);
                    var option={
                        tooltip: {
                            trigger: 'item',
                        },
                        legend: {
                            bottom: '5%',
                            left: 'center',
                        },
                        title:{
                            text:"Complaints"
                        },
                        series:[{
                            name: 'Complaints',
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
                                position:'center'
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
                        }]
                    };

                    Chart.setOption(option);
                })
                .catch(function (error) {
                    console.log(error);
                });
            
        },
    },
    mounted(){
        this.EchartsOperatorStatus();
        this.EchartsComplaintsStatus();
    }
}
</script>