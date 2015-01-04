var massiveApp = angular.module('massiveApp', [
    'ngResource',
    'ui.bootstrap'
    //'ngRoute'
]);

massiveApp.factory('Links', ['$resource',function ($resource) {
    var links = $resource(
        '/links', {}, {
                        'save':{method:'POST'},
                        'query':{cache:false,isArray:true}
                    }
    );
    return links
}]);

massiveApp.controller('LinksListCtrl',['$scope','$modal','$http','Links',
    function($scope,$modal,$http,Links) {
        $scope.links = Links.query()

        $scope.remove = function(_id){
            console.log(_id)
            $http.delete('/links/' + _id).success(function(r){
                $scope.links = Links.query()
            })
        }

        //---------------- modal -----------
        $scope.open = function () {
            var modalInstance = $modal.open({
                templateUrl: 'partials/modal.html',
                controller: ModalInstanceCtrl,
            });

            modalInstance.result.then(function (Links) {
                $scope.links = Links.query()
            })
        }
    }
]);

massiveApp.directive('ngTag', function() {
    return {
        restrict: 'A',
        require: ['^ngModel'],
        scope: {
            ngModel: '='
        },
        controller: ['$scope', '$http', function($scope, $http) {
            $scope.newTags = undefined;
            $scope.isCollapsed = true;

            $scope.toggleAddTags = function(){
                if ($scope.isCollapsed == true)
                    $scope.isCollapsed = false
                else
                    $scope.isCollapsed = true
            }

            $scope.addTags = function(_id){
                if(_id != undefined){
                    var data = {
                        tags : $scope.newTags.split(",")
                    }
                    $http.post('/links/' + _id, data).success(function(r){
                        $scope.ngModel.tags = r.tags
                        $scope.toggleAddTags()
                    })
                }
            }

        }],

        // link: function(scope, iElement, iAttrs, ctrl) {
        //     //console.log(scope.ngModel)
        //     return undefined
        // },
        templateUrl: 'template/ngtag.html'
    }
});

var ModalInstanceCtrl = function ($scope, $modalInstance, $http) {
    $scope.url = ""
    $scope.tags = ""

    $scope.ok = function () {
        var data = {
            tags: $scope.tags.split(','),
            url: $scope.url
        }
        $http.post('/links', data)//.success(function(){});
        $modalInstance.dismiss('cancel');
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };


};
