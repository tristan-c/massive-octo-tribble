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

massiveApp.controller('LinksListCtrl',['$scope','$modal','Links',
    function($scope,$modal,Links) {
        $scope.links = Links.query()

        //---------------- modal -----------
        $scope.open = function () {
            var modalInstance = $modal.open({
                templateUrl: 'partials/modal.html',
                controller: ModalInstanceCtrl,
                //size: size,
                resolve: {
                    items: function () {
                        return $scope.items;
                    }
                }
            });

            // modalInstance.result.then(function (selectedItem) {
            //     $scope.selected = selectedItem;
            // }, function () {
            //     console.log('Modal dismissed at: ' + new Date());
            // });
        }

    }
]);

var ModalInstanceCtrl = function ($scope, $modalInstance, items) {
    $scope.items = [];

    $scope.ok = function () {
        $modalInstance.close($scope.selected.item);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
};