
# user temporary dashboard route
@app.route('/token_ok')
@token_required
def token_ok(current_user):
    if not current_user:
        return jsonify({'message': 'Cannot perform that function! Please login'})

    response = jsonify({"message": "Yeaah!! You have successfully authenticated your token"})
    return response