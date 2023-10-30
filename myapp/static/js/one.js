const forms=document.getElementById('forms')
const username=document.getElementById('username')
const email=document.getElementById('email')

forms.addEventListener('submit',e=>{
  e.preventDefault();
  validateInputs();
});

const validateInputs=() =>{
  const usernameValue=username.
}


var stripe=Stripe('{{stripe_publishable_key}')
var checkoutButton=document.getElementById('checkout')
checkoutButton.addEventListener('click',function(){
  fetch("{% url 'myapp:api_checkout_session' id=product.id %}",{method:'POST',})
  .then(function(response){
    return response.json()
  })
  .then(function(session){
    return stripe.redirectToCheckout({sessionId:session.sessionId})
  })
  .then(function(result){
     if (result.error){
      alert(result.error.message)
     }
  })
  .catch(function(error){
    console.error('Error',error)
  })
})