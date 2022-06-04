$("button#generate").click(function () {
    // 多重送信を防ぐため通信完了までボタンをdisableにする
    var button = $(this);
    button.attr("disabled", true);

    // 各フィールドから値を取得してJSONデータを作成
    var data = {
        url: $("#url").val()
    };

    // 通信実行
    $.ajax({
        type: "post",                // method = "POST"
        url: "http://localhost:8000/generate/",        // POST送信先のURL
        async: true, // 非同期通信フラグの指定
        data: JSON.stringify(data),  // JSONデータ本体
        contentType: 'application/json', // リクエストの Content-Type
        dataType: "json",           // レスポンスをJSONとしてパースする
        success: function (json_data) {   // 200 OK時
            // JSON Arrayの先頭が成功フラグ、失敗の場合2番目がエラーメッセージ
            if (!json_data[0]) {    // サーバが失敗を返した場合
                alert("Transaction error. " + json_data[1]);
                return;
            }
            // 成功時処理
            location.reload();
        },
        error: function () {         // HTTPエラー時
            alert("Server Error. Please try again later.");
        },
        complete: function () {      // 成功・失敗に関わらず通信が終了した際の処理
            button.attr("disabled", false);  // ボタンを再び enableにする
        }
    });
});