(function() {
    
    const playButton = document.getElementById("play-round")
    playButton.addEventListener('click', function(){
        fetch('/invoice', {
            method: 'POST',
            headers: {
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        })
        .then(function(res){ return res.json()})
        .then(function(response){
            if(response.invoice_url){
                lpPayments.init({
                    frameUrl: response.invoice_url,
                    onPaymentComplete: function(){
                        window.location.href = "/round/" + response.invoice_id
                    },
                    onPaymentFailed: function(){
                        window.location.reload()
                    }
                })
            }
        });
    })

    const claimElements = document.querySelectorAll('.claim')
    if(claimElements){
        claimElements.forEach(function(element){
            element.addEventListener('click', function(){
                lpPayments.init({
                    frameUrl: element.getAttribute('data-claim-url'),
                    onPaymentComplete: function(){
                        alert("Refund successful")
                    },
                    onPaymentFailed: function(){
                        alert("Refund failed, please try again")
                    }
                })
            })
        })
    }
})();