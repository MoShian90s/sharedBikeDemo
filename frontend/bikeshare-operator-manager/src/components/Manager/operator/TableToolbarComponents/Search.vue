<template>
<el-card  class='box-card' shadow='always' body-style="display:flex;justify-content:center;align-items:center;padding:5% 7% 5% 7%">
	<el-form size="medium" style="width:100%">
		<el-form-item>
			<el-select v-model="SelectField" placeholder="field" style="width:100%">
				<el-option label="🆔 Unique ID" value="id"></el-option>
				<el-option label="🔠 Name" value="Username"></el-option>
				<el-option label="👩‍💻 Status" value="Login_status"></el-option>
			</el-select>
		</el-form-item>
		<el-form-item>
			<el-input placeholder="Search Key Word" v-model="keyword" v-show="TextVisible"></el-input>
			<el-select v-model="keyword" placeholder="choose the status" style="width:100%" v-show="SelectVisible">
				<el-option label="🔹 Online" value='1'></el-option>
				<el-option label="🔸 Offline" value='0'></el-option>
			</el-select>
		</el-form-item>
		<el-form-item>
			<el-button icon='el-icon-search' round class='SearchBtn' @click.native='Search'>Search</el-button>
		</el-form-item>
	</el-form>
</el-card>
</template>

<script>
import axios from 'axios';
import qs from 'qs';
import {sharedStore} from '../Table'

export default {
    data(){
        return{
            keyword:'',
			SelectField:'id',
        }
    },
	computed:{
		SelectVisible:function(){
			if(this.SelectField==='Login_status'){
				return true;
			}else{
				return false;
			}
		},
		TextVisible:function(){
			if(this.SelectVisible){
				return false;
			}else{
				return true;
			}
		}
	},
    methods:{
        Search(){
            let that=this;
			
            let payload=qs.stringify({type:that.SelectField,keyword:that.keyword});
            axios.post(that.$baseURL+"/manager/searchoperatorinfo/",payload)
                .then(function(response) {
                    let data=[];
                    response.data.forEach(element => {
						let item=element['fields']
						item['id']=element['pk']
                        data.push(item)
                    });
                    sharedStore.tableData=data;
                    that.$notify.success({
                        title:'Search Operation',
                        message:'system is returning ' + that.SelectField
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
.SearchBtn{
    width:100%;
    margin-top:3vh;
}
.SearchBtn:hover{
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
}
.scale-in-center {
	-webkit-animation: scale-in-center 0.5s cubic-bezier(0.250, 0.460, 0.450, 0.940) both;
	animation: scale-in-center 0.5s cubic-bezier(0.250, 0.460, 0.450, 0.940) both;
}
@-webkit-keyframes scale-in-center {
  0% {
    -webkit-transform: scale(0);
            transform: scale(0);
    opacity: 1;
  }
  100% {
    -webkit-transform: scale(1);
            transform: scale(1);
    opacity: 1;
  }
}
@keyframes scale-in-center {
  0% {
    -webkit-transform: scale(0);
            transform: scale(0);
    opacity: 1;
  }
  100% {
    -webkit-transform: scale(1);
            transform: scale(1);
    opacity: 1;
  }
}

.scale-out-center {
	-webkit-animation: scale-out-center 0.5s cubic-bezier(0.550, 0.085, 0.680, 0.530) both;
	animation: scale-out-center 0.5s cubic-bezier(0.550, 0.085, 0.680, 0.530) both;
}
@-webkit-keyframes scale-out-center {
  0% {
    -webkit-transform: scale(1);
            transform: scale(1);
    opacity: 1;
  }
  100% {
    -webkit-transform: scale(0);
            transform: scale(0);
    opacity: 1;
  }
}
@keyframes scale-out-center {
  0% {
    -webkit-transform: scale(1);
            transform: scale(1);
    opacity: 1;
  }
  100% {
    -webkit-transform: scale(0);
            transform: scale(0);
    opacity: 1;
  }
}
</style>