<template>
    <div>
        <ve-table 
            class="VeTable custable" 
            row-key-field-name="Customer_id"
            :columns="columns"
            :table-data="tableData"
            :event-custom-option="eventCustomOption"
            :virtual-scroll-option="virtualScrollOption"
            :max-height="700"/>
    </div>
</template>

<script>
import axios from 'axios';
import Vue from 'vue';
axios.defaults.withCredentials=true;

export default {
    props:{
        notifyUpdate:Number,
    },
    watch:{
        notifyUpdate:function(){
            this.refresher();
        },
        rowMsg:function(){
            this.$emit("select",this.rowMsg);
        }
    },
    computed:{
        tableData:function(){
            return sharedStore.tableData;
        }
    },
    data(){
        return{
            virtualScrollOption: {
                enable: true,
            },
            toolbarVisible:false,
            rowMsg:[],
            columns: [
                {field: "", title:'', width: '5%', align: "center",renderBodyCell:({rowIndex})=>{return ++rowIndex;}},
                {field: "Customer_id", title:'Unique ID', align: "center"},
                {field: "Customer_first_name", title:'First Name', align: "center"},
                {field: 'Customer_last_name', title:'Last Name', align: "center"},
                {field: 'Customer_age', title: 'Age', align: "center"},
                {field: 'Customer_gender', title: 'Gender', align: "center"},
                {field: 'Customer_phone_num', title: 'Phone', align: "center"},
            ],
            eventCustomOption: {
                bodyRowEvents: ({ row, rowIndex }) =>{
                    let that=this;
                    return {
                        click: (event) => {
                            console.log("table-click::", row, rowIndex, event);
                            that.rowMsg=row;
                        },

                    };
                }
            },
        }
    },
    methods:{
        refresher(){
            let that=this;
            axios.get(that.$baseURL+'/manager/retrievecustomerinfo/')
                .then(function(response) {
                    // that.tableData = response.data;
                    let data=[];
                    response.data.forEach(element => {
                        data.push(element['fields'])
                    });
                    sharedStore.tableData=data;
                })
                .catch(function (error) {
                    console.log(error);
            });
        }
    },
    mounted:function(){
        this.refresher();
    }
}

export var sharedStore=Vue.observable({tableData:[]});
</script>

<style scoped>
.custable{
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)!important;
}
</style>