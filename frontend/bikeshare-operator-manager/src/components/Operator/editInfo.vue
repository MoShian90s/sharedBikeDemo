<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">home</el-breadcrumb-item>
      <el-breadcrumb-item>edit information</el-breadcrumb-item>
    </el-breadcrumb>
    <h3>hello,operator {{Operator_id}}</h3>
    <el-form ref="form" :model="form" :rules="rules" label-width="80px">
      <el-form-item label="username" prop="username" label-width="120px">
        <el-input v-model="form.username" width="120px" readonly></el-input>
      </el-form-item>
      <el-form-item label="old password" prop="oldpassword" label-width="120px">
        <el-input type="password" v-model="form.oldpassword" width="120px" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item label="new password" prop="password" label-width="120px">
        <el-input type="password" v-model="form.password" width="120px" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item label="enter again" prop="password2" label-width="120px">
        <el-input type="password" v-model="form.password2" width="120px" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">save and modify</el-button>
      </el-form-item>
    </el-form>

  </div>
</template>

<script>
  import qs from 'qs'
  export default {
    data() {
      var validatePass2 = (rule, value, callback) => {
        if (value !== this.form.password) {
          callback(new Error("the two new password should be same"));
        } else {
          callback();
        }
      };
      return {
        form: {
          username: this.$session.get("username"),
          oldpassword: '',
          password: '',
          password2: ''
        },
        Operator_id: 0,
        rules: {
          username: [{
            required: true,
            message: "enter username",
            trigger: "blur"
          }, {
            min: 1,
            max: 10,
            message: "between 1-10 letters",
            trigger: "blur"
          }],
          oldpassword: [{
            required: true,
            message: "enter the old password",
            trigger: 'blur'
          }],
          password: [{
            required: true,
            message: "enter the new password",
            trigger: 'blur'
          }, {
            min: 5,
            max: 10,
            message: "the length should between 5-10 letters",
            trigger: 'blur'
          }],
          password2: [{
            required: true,
            message: "enter the new password again",
            trigger: "blur"
          }, {
            validator: validatePass2,
            trigger: "blur"
          }]
        },
        total: 1,
        id: 123,
      }
    },
    mounted() {
      this.Operator_id = this.$session.get("Operator_id")
      // this.username=this.$session.get("username")
    },
    methods: {
      onSubmit() {
        let that = this
        var fdata = qs.stringify({
          "username": this.form.username,
          "old_password": this.form.oldpassword,
          "new_password": this.form.password
        })
        console.log(this.$data.form)
        this.$refs.form.validate((valid => {
          if (valid) {
            if(this.form.password.length<5){
              that.$message('new password is short, we recommend lenght of 5 at least')
            }else if (this.form.oldpassword == this.form.password) {
              that.$message("new password and old password should be different")
            }else if (this.form.password != this.form.password2) {
              that.$message("new password and enter again should be same")
            } else {
              this.$axios
                .post(this.$baseURL+'/operator/editprofile/', fdata)
                .then(function(result) {
                  console.log(result);
                  that.$message.info(result.data);
                  that.form.oldpassword = ''
                  that.form.password = ''
                  that.form.password2 = ''
                }).catch(function(err) {
                  console.log(err);
                })
            }
          } else {}
        }))
      }
    },
  }
</script>

<style scoped>
.el-card{
	box-shadow: 0 1px 1px rgba(0,0,0,0.15) !important;
}
</style>
