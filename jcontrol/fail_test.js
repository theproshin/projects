// -------- Панель массовых операций --------

    // сохранение результатов через панель массовых операций
    $scope.SaveMassTestsResult = function(save_edit) {
        var panel = $scope.MassOperation;
        panel.typeValidError = !panel.typeError;
        panel.descValidError = !panel.description;
        if (panel.typeValidError || panel.descValidError) {
            return
        }
        if (panel.typeError ===1 && !panel.description.match(re)) {
            $scope.Alert = {
                show: true,
                text: 'Нет ссылки на задачу',
                success: false
            }
            return


        }
        var results = [];
        angular.forEach($scope.results, function(result) {
            var suite = result.suite;
            for (var i in result.tests) {
                var test = result.tests[i];
                if (test.select) {
                    if (!test.description || !test.type_err || save_edit) {
                        test.type_err = panel.typeError;
                        test.description = panel.description;
                        test.err_type = false;
                        results.push([suite, test.test, test.type_err, test.description])
                    }
                    else {
                        if (!save_edit) {
                            $scope.ConfirmDialog = {
                                show: true,
                                text: 'Перезаписать уже сохранненные записи?',
                                yes: function () {
                                    $scope.SaveMassTestsResult(true)
                                },
                                no: $scope.UnSelectAndCloseAlert
                            };
                            return
                        }
                    }
                }
            }
            result.select = false;
        });
        // если есть что сохранить, то сохраняем
        if (results.length) {
            $scope.SelectAll = false;
            SaveTestsResult(results)
        }
        if (!$scope.ConfirmDialog.show || save_edit) {
            $scope.SelectAll = false;
            panel.typeValidError = '';
            panel.descValidError = '';
            panel.description = '';
            if (save_edit) {
                $scope.ConfirmDialog.show = false;
            }
        }
    };
