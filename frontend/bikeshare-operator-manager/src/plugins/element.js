import Vue from 'vue'
import 'element-ui/lib/theme-chalk/index.css'
import {
  Button,
  Form,
  FormItem,
  Input,
  Message,
  Container,
  Header,
  Aside,
  Main,
  Menu,
  Submenu,
  MenuItem,
  Breadcrumb,
  BreadcrumbItem,
  Card,
  Row,
  Col,
  Table,
  TableColumn,
  Select,
  Option,
  Dialog,
  MessageBox,
  DatePicker,
  Tag,
  Pagination,
  Tooltip,
  Divider,
  Link,
  Avatar,
  Drawer,
  Switch,
  Slider,
  Notification,
} from 'element-ui'
import lang from 'element-ui/lib/locale/lang/en'
import locale from 'element-ui/lib/locale'
Vue.prototype.$message = Message
Vue.prototype.$confirm = MessageBox.confirm
Vue.prototype.$notify= Notification
locale.use(lang)
Vue.use(Button)
Vue.use(Form)
Vue.use(FormItem)
Vue.use(Input)
Vue.use(Container)
Vue.use(Header)
Vue.use(Aside)
Vue.use(Main)
Vue.use(Menu)
Vue.use(Submenu)
Vue.use(MenuItem)
Vue.use(Breadcrumb)
Vue.use(BreadcrumbItem)
Vue.use(Card)
Vue.use(Row)
Vue.use(Col)
Vue.use(Table)
Vue.use(TableColumn)
Vue.use(Select)
Vue.use(Option)
Vue.use(Dialog)
Vue.use(DatePicker)
Vue.use(Tag)
Vue.use(Pagination)
Vue.use(Drawer)
Vue.use(Avatar)
Vue.use(Divider)
Vue.use(Link)
Vue.use(Tooltip)
Vue.use(Switch)
Vue.use(Slider)
