<template>
    <div>
        <ve-table 
            class="VeTable optable" 
            row-key-field-name="id"
            :columns="columns"
            :table-data="tableData"
            :event-custom-option="eventCustomOption"
            :virtual-scroll-option="virtualScrollOption"
            :max-height="800"/>
        <span style="font-size:5rem;both:clear;display:flex;justify-content:center">🚲🚲🚲🚲🚲🚲🚲</span>
    </div>
</template>

<script>
import axios from 'axios';
import Vue from 'vue';

export default {
    data(){
        return{
            virtualScrollOption: {  
                enable: true,
            },
            toolbarVisible:false,
            rowMsg:[],
            columns: [
                {field: "", title:'', width: '5%', align: "center",renderBodyCell:({rowIndex})=>{return ++rowIndex;}},
                {field: 'Username', title:'name', align: "center"},
                {field: 'id', title:'id', align: "center"},
                {field: 'Login_status', title: 'status', align: "center",
                    renderBodyCell: ({ row, column}) => {
                        let status=row[column.field];
                        var flag="success";
                        var text="online";
                        if(status===false){
                            flag="danger"
                            text="offline"
                        }
                        return (
                            <el-tag type={flag} style="padding:0 10px">{text}</el-tag>
                        );
                    },},
            ],
            eventCustomOption: {
                bodyRowEvents: ({ row, rowIndex }) =>{
                    let that=this;
                    return {
                        click: (event) => {
                            console.log("table-click::", row, rowIndex, event);
                            that.rowMsg=row;
                            that.toolbarVisible=true;
                        },

                    };
                }
            },
            
        }
    },
    computed:{
        tableData:function(){
            return sharedStore.tableData;
        }
    },
    mounted:function(){
        let that=this;
        sharedStore.refresher(that.$baseURL)
    }
}

export var sharedStore=Vue.observable({
    tableData:[],
    refresher:function(url){
        // let that=this;
        axios.get(url+'/manager/retrieveoperatorinfo/')
            .then(function(response) {
                let data=[];
                response.data.forEach(element => {
                    let item=element['fields']
                    item['id']=element['pk']
                    data.push(item)
                });
                sharedStore.tableData=data;
            })
            .catch(function (error) {
                console.log(error);
        });
    }})
</script>

<style scoped>
.optable{
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)!important;
    margin-bottom: 10vh;
}
</style>