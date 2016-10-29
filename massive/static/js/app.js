window.eventBus = new Vue();

Vue.component('modal', {
  template: '#modal-template',
  data : function(){
    return {
        url: "",
        tags: ""
      }
  },
  methods: {
    save:function(){
        var me = this,
	    http = new XMLHttpRequest(),
            params = "";

        http.open("POST", "/links", true);
        http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        
        params += "url=";
        params += encodeURIComponent(this.url);
        params += "&tags=";
        params += encodeURIComponent(this.tags);

        http.send(params);
        me.$emit("close");
	window.eventBus.$emit('reload');
    }
  }
})

var app = new Vue({
    el: '#app',
    data: {
        links: [],
        filteredLinks: [],
        search: "",
        showModal: false,
        showSpinner: false
    },
    created: function() {
        this.fetchData();
	window.eventBus.$on('reload',this.fetchData);
    },
    methods: {
        fetchData: function() {
            var xhr = new XMLHttpRequest()
            var me = this
            xhr.open('GET', "/links")
            xhr.onload = function() {
                var data = JSON.parse(xhr.responseText);
                me.links = data;
                me.filteredLinks = data;
                me.showSpinner = false;
            }
            me.showSpinner = true;
            xhr.send();
        },
        remove: function(linkId){
            var xhr = new XMLHttpRequest(),
	        me  = this;
            xhr.open('DELETE', "/links/" + linkId)
            xhr.send()
	    me.fetchData()
        }
    },
    watch: {
        search: function() {
            var me = this
            me.filteredLinks = me.links.filter(function(item) {
                var searchRegex = new RegExp(me.search, 'i')
                for(var i = 0 ; i < item.tags.length ; i++)
                    if(searchRegex.test(item.tags[i]))
                        return true
                if(searchRegex.test(item.url))
                    return true;
                if(searchRegex.test(item.title))
                    return true
                return false
            })
        }
    }
})



//jquery part
