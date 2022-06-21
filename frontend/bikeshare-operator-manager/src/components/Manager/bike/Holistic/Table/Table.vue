<template>
    <div>
        <ve-table 
            class="VeTable custable" 
            row-key-field-name="id"
            :columns="columns"
            :table-data="tableData"
            :event-custom-option="eventCustomOption"
            
            :max-height="700"/>
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
                {field: 'Insurance_id', title:'Unique ID', align: "center"},
                {field: 'Brand', title:'Brand', align: "center"},
                {field: 'Original_loc_lat', title: 'Latitude', align: "center"},
                {field: 'Original_loc_long', title: 'Longtitude', align: "center"},
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
        axios.get(that.$baseURL+'/manager/retrievebikeinfo/')
            .then(function(response) {
                let data=[];
                response.data.forEach(element => {
                    data.push(element['fields'])
                });
                sharedStore.tableData=data;
            })
            .catch(function (error) {
                console.log(error);
        });
    },
}

export var sharedStore=Vue.observable({tableData:[]})
</script>

<style scoped>
.custable{
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)!important;
}
</style>