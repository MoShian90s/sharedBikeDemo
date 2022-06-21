<template>
    <el-row :gutter="50" type="flex" style="flex-wrap:wrap">
        <el-col :xs='24' :sm='24' :md='24' :lg='24' :xl='24'>
            <el-card  class='box-card' shadow='always' body-style="display:flex;justify-content:center;align-items:center;padding:5% 7% 5% 7%">
                <!-- search form -->
                <el-form size="medium" style="width:100%">
                    <el-form-item>
                        <el-select v-model="form.SelectField" placeholder="field" style="width:100%">
                            <el-option label="🆔 Unique ID" value="Insurance_id"></el-option>
                            <el-option label="🚲 Brand" value="Brand"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item>
                        <el-input placeholder="Search Key Word" v-model="keyword"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button icon="el-icon-search" round class="SearchBtn" @click.native="Search">Search</el-button>
                    </el-form-item>
                </el-form>
            </el-card>
        </el-col>
    </el-row>
</template>

<script>
import axios from 'axios';
import qs from 'qs'
import {sharedStore} from './Table'

export default {
    data(){
        return{
            form:{
                SelectField:'Insurance_id',
            },
            keyword:'',
        }
    },
    methods:{
        Search(){
            let that=this;
            let payload=qs.stringify({type:that.form.SelectField,keyword:that.keyword});
            axios.post(that.$baseURL+"/manager/searchbikeinfo/",payload)
                .then(function(response) {
                    let data=[];
                    response.data.forEach(element => {
                        data.push(element['fields'])
                    });
                    sharedStore.tableData=data;
                    that.$notify.success({
                        title:'Search Operation',
                        message:'system is returning ' + that.keyword
                    });
                })
                .catch(function () {
                    that.$notify.error({
                        title:'Search Operation',
                        message:'no results found'
                    });
            });
        }
    }
}
</script>

<style scoped>
.el-card{
    margin-bottom:5vh;
}
.SearchBtn{
    width:100%;
    margin-top:3vh;
}
.SearchBtn:hover{
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
}
</style>